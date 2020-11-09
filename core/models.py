from django.db import models
from django.shortcuts import get_object_or_404


class SiteConfiguration(models.Model):
    """
    Singleton for the site configuration
    """
    probability_threshold = models.FloatField()
    max_associated_topics = models.IntegerField()

    @staticmethod
    def get_configuration():
        return get_object_or_404(SiteConfiguration, pk=1)


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Document(models.Model):

    def __init__(self, topic_match = None, *args, **kwargs):
        super(Document, self).__init__(*args, **kwargs)
        self.topic_match = topic_match

    TYPE_CHOICES = [
        ("tweet", "Twitter"),
    ]

    TOPIC_MATCH_COLORS = ["#d9534f", "#f0ad4e", "#5bc0de", "#5cb85c"]

    url_identifier = models.CharField(max_length=500, unique=True)
    url = models.CharField(max_length=500)
    doi = models.CharField(max_length=64)
    title = models.CharField(max_length=500)
    text = models.TextField()
    date = models.DateField()
    type = models.CharField(choices=TYPE_CHOICES, max_length=16)
    tags = models.ManyToManyField(Tag, related_name="documents")

    @property
    def topic_match_color(self):
        if self.topic_match is None:
            return None
        else:
            return self.TOPIC_MATCH_COLORS[min(len(self.TOPIC_MATCH_COLORS)-1, self.topic_match//25)]


class Topic(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)


class DocumentInTopic(models.Model):
    """
    Model not defined as a though table because we want the probability threshold to be
    changeable on the website
    """
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    probability = models.FloatField()


class OriginalTopicProbabilities(models.Model):
    """
    Model for storing the
    """

