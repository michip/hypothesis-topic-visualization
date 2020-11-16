from django.db import models
from django.shortcuts import get_object_or_404


class SiteConfiguration(models.Model):
    """
    Singleton for the site configuration
    """
    probability_threshold = models.FloatField()
    max_associated_topics = models.IntegerField()
    active_topic_model = models.ForeignKey('TopicModel', on_delete=models.SET_NULL, null=True)

    @staticmethod
    def get_configuration():
        return SiteConfiguration.objects.get(pk=1)


class Tag(models.Model):
    name = models.CharField(max_length=100)


class Document(models.Model):

    TYPE_CHOICES = [
        ("tweet", "Twitter"),
        ("webpage", "Webpage"),
        ("preprint", "Preprint"),
        ("news", "News"),
        ("youtube", "YouTube"),
        ("report", "Report"),
        ("blog", "Blog"),
    ]

    url_identifier = models.CharField(max_length=500, unique=True)
    url = models.CharField(max_length=500)
    doi = models.CharField(max_length=500, blank=True)
    title = models.TextField(blank=True)
    text = models.TextField()
    date = models.DateField()
    document_type = models.CharField(choices=TYPE_CHOICES, max_length=16, default="blog")
    tags = models.ManyToManyField('Tag', related_name="documents")

    @property
    def original_topic_relationships(self):
        return OriginalTopicProbabilities.objects.filter(document=self).order_by('-probability')

    def __str__(self):
        return self.url_identifier

class Keyword(models.Model):
    value = models.CharField(max_length=128)
    topic = models.ForeignKey('Topic', related_name='keywords', on_delete=models.CASCADE)

    def __str__(self):
        return self.value


class TopicModel(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.created_at})"


class Topic(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    documents = models.ManyToManyField(Document, through='DocumentInTopic', related_name="topics")
    topic_model = models.ForeignKey(TopicModel,
                                    on_delete=models.CASCADE,
                                    related_name='topics', null=True)

    @staticmethod
    def get_active_topics():
        return Topic.objects.filter(topic_model=SiteConfiguration.get_configuration().active_topic_model)

    def __str__(self):
        return self.name

class DocumentInTopic(models.Model):
    """
    Model not defined as a though table because we want the probability threshold to be
    changeable on the website
    """
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    probability = models.FloatField()

    def __str__(self):
        return f"{self.document}-{self.topic}:{self.probability}"


class OriginalTopicProbabilities(models.Model):
    """
    Model for storing the full topic probabilities, so this won't be used as a topic-document relation
    """
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    probability = models.FloatField()

