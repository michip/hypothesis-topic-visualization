import faker
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hypothesis_topic_visualization.settings')
import django
django.setup()
from datetime import datetime
from core.models import *
import random as rd

fake = faker.Faker()

Document.objects.all().delete()
Topic.objects.all().delete()
OriginalTopicProbabilities.objects.all().delete()
DocumentInTopic.objects.all().delete()

topics = []
for i in range(10):
    topic = Topic(name=fake.text(max_nb_chars=rd.randint(10, 30)),
                  description=fake.text(max_nb_chars=rd.randint(100, 250)))
    topic.save()

    topics.append(topic)

for i in range(50):
    doc = Document(url_identifier="" + str(i),
                   url="https://twist.com/a/131368/ch/391926/t/1996519/",
                   doi="https://doi.org/10.1257/aer.101.3.318",
                   title=fake.text(max_nb_chars=rd.randint(20, 50)),
                   text=fake.text(max_nb_chars=rd.randint(100, 250)),
                   date=datetime.now().date(),
                   type="tweet")
    doc.save()

    topic_probs = [rd.random() for _ in range(len(topics))]
    topic_probs = [k/sum(topic_probs) for k in topic_probs]

    for k, topic in zip(topic_probs, topics):
        orig = OriginalTopicProbabilities(document=doc, topic=topic, probability=k)
        orig.save()

