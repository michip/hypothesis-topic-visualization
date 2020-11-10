from django.shortcuts import render, get_object_or_404
from .models import *
import datetime
import random as rd
from django.contrib import messages

def home(request):
    return render(request, "core/home.html", dict(
        topics=Topic.objects.all(), document_count=Document.objects.count()))


def configuration(request):
    if request.method == "GET":
        return render(request, 'core/configuration.html')
    elif request.method == "POST":
        config = SiteConfiguration.get_configuration()

        try:
            threshold = float(request.POST.get("threshold", ""))
            topic_amount = int(request.POST.get("topicAmount", ""))
        except ValueError:
            messages.error(request, "Please enter a valid threshold and max amount!")
            return render(request, 'core/configuration.html')

        config.probability_threshold = threshold
        config.max_associated_topics = topic_amount
        config.save()

        DocumentInTopic.objects.all().delete()

        for doc in Document.objects.all():
            orig_probs = OriginalTopicProbabilities.objects.filter(document=doc).order_by("-probability")[
                         :config.max_associated_topics]

            current_value = 0
            for orig_prob in orig_probs:
                if current_value < config.probability_threshold:
                    print(orig_prob.document, orig_prob.topic, orig_prob.probability)
                    document_in_topic = DocumentInTopic(document=doc,
                                    topic=orig_prob.topic, probability=orig_prob.probability)
                    document_in_topic.save()
                    current_value += orig_prob.probability

        messages.success(request, "Configuration updated successfully!")

        return render(request, 'core/configuration.html')


def topic_overview(request):
    return render(request, "core/topic_overview.html", dict(topics=Topic.objects.all()))


def topic(request, id):
    current_topic = get_object_or_404(Topic, pk=id)
    documents_in_topic = DocumentInTopic.objects.filter(topic=current_topic).order_by("-probability")
    return render(request, "core/topic.html", dict(topic=current_topic, documents_in_topic=documents_in_topic))