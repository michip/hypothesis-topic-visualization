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

    TYPE_CHOICES = [
        ("tweet", "Twitter"),
    ]

    url_identifier = models.CharField(max_length=500, unique=True)
    url = models.CharField(max_length=500)
    doi = models.CharField(max_length=64)
    title = models.CharField(max_length=500)
    text = models.TextField()
    date = models.DateField()
    type = models.CharField(choices=TYPE_CHOICES, max_length=16)
    tags = models.ManyToManyField(Tag, related_name="documents")


class Topic(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    documents = models.ManyToManyField(Document, through='DocumentInTopic')


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
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    probability = models.FloatField()

