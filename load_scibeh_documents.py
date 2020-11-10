import argparse
import json
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hypothesis_topic_visualization.settings')
import django

django.setup()

from datetime import datetime
from core.models import *
import random as rd
from tqdm import tqdm
import faker

parser = argparse.ArgumentParser()

parser.add_argument('-f', '--file', required=True)
parser.add_argument('--clear', action='store_true')

args = parser.parse_args()

if args.clear:
    Document.objects.all().delete()
    Tag.objects.all().delete()

with open(args.file, 'r') as f:
    document_json = json.load(f)

fake = faker.Faker()
topics = []
for i in range(10):
    topic = Topic(name=fake.text(max_nb_chars=rd.randint(10, 30)),
                  description=fake.text(max_nb_chars=rd.randint(100, 250)))
    topic.save()

    topics.append(topic)

for doc in tqdm(document_json):

    arguments = dict(url_identifier=doc['id'],
                     url=doc['url'],
                     title=doc['title'],
                     text=doc['summary'],
                     date=datetime.strptime(doc['date'], '%Y-%m-%d'),
                     document_type=doc['type'])

    if "doi" in doc:
        arguments["doi"] = doc["doi"]

    document = Document.objects.create(**arguments)

    if "tags" in doc:
        for tag in doc["tags"]:
            t, _ = Tag.objects.get_or_create(name=tag)
            document.tags.add(t)
            t.save()

    topic_probs = [rd.random() for _ in range(len(topics))]
    topic_probs = [k / sum(topic_probs) for k in topic_probs]

    for k, topic in zip(topic_probs, topics):
        orig = OriginalTopicProbabilities(document=document, topic=topic, probability=k)
        orig.save()
