import os
import json
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hypothesis_topic_visualization.settings')
import django
django.setup()
from core.models import OriginalTopicProbabilities
from tqdm import tqdm
OriginalTopicProbabilities.objects.all().delete()

with open('probabilities.json', 'r') as f:
    data = json.load(f)


probability_objects = []
for prob in tqdm(data):
    prob['fields']['document_id'] = prob['fields']['document']
    prob['fields']['topic_id'] = prob['fields']['topic']
    del prob['fields']['topic'], prob['fields']['document']
    t = OriginalTopicProbabilities(**prob['fields'])
    probability_objects.append(t)

OriginalTopicProbabilities.objects.bulk_create(probability_objects)