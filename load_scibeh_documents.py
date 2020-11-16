import argparse
import json
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hypothesis_topic_visualization.settings')
import django

django.setup()

from datetime import datetime
from core.models import *
from tqdm import tqdm

parser = argparse.ArgumentParser()

parser.add_argument('-f', '--documents-file', required=True)
parser.add_argument('-t', '--topics-file', required=True)
parser.add_argument('-n', '--model-name', required=True)
parser.add_argument('--clear-topics', action='store_true')
parser.add_argument('--clear-documents', action='store_true')

args = parser.parse_args()

if args.clear_documents:
    Document.objects.all().delete()
    Tag.objects.all().delete()

if args.clear_topics:
    Topic.objects.all().delete()

with open(args.documents_file, 'r') as f:
    document_json = json.load(f)

with open(args.topics_file, 'r') as f:
    topics_json = json.load(f)

topics = []

topic_model = TopicModel.objects.create(name=args.model_name)

for top in topics_json["topics"]:
    topic, created = Topic.objects.get_or_create(name=top['title'],
                                                 description=top['description'],
                                                 topic_model=topic_model)

    if created:
        for keyword in top["keywords"]:
            if isinstance(keyword, list):
                keyword = keyword[0]
            Keyword.objects.get_or_create(value=keyword, topic=topic)

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

    document, created = Document.objects.get_or_create(**arguments)

    if created and "tags" in doc:
        for tag in doc["tags"]:
            t, _ = Tag.objects.get_or_create(name=tag)
            document.tags.add(t)
            t.save()

for topics_assigment in tqdm(topics_json["documents"]):
    document = Document.objects.get(url_identifier=topics_assigment["id"])

    for k, topic in zip(topics_assigment["topics"], topics):
        if isinstance(k, list):
            k = k[0]

        OriginalTopicProbabilities.objects.get_or_create(document=document, topic=topic, probability=k)
