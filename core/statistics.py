from .models import Topic
from django.db.models.functions import ExtractWeek, ExtractYear
from django.db.models import Sum, Count
from django.db.models.functions import ExtractWeek, ExtractYear
import json


class TopicStatistic:

    def __init__(self, topic: Topic):
        self.topic = topic

    @property
    def papers_per_week(self):
        documents = self.topic.documents
        documents = documents.annotate(year=ExtractYear('date')) \
            .annotate(week=ExtractWeek('date')) \
            .values('year', 'week').order_by('year', 'week') \
            .annotate(count=Count('*'))

        data = []
        total = 0

        for record in documents:
            week = "{year}-W{week}".format(year=record['year'], week=record['week'])
            count = record['count']
            total += count
            data.append((week, count, total))

        data = list(zip(*data))

        return json.dumps(dict(weeks=data[0], counts=data[1], totals=data[2]))
