from django.shortcuts import render, get_object_or_404
from .models import *
import datetime
import random as rd
from django.contrib import messages


def get_random_topic():
    return Topic(pk=2,
                 name="XYZ",
                 description="Lorem ipsum dolor sit amet, consetetur sadipscing elitr, se")

def get_random_document():
    return Document(
        url="https://twist.com/a/131368/ch/391926/t/1996519/",
        doi="https://doi.org/10.1257/aer.101.3.318",
        title="Trusted Decision-Making: Data Governance for Creating Trust in Data Science Decision Outcomes",
        text="Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.",
        date=datetime.datetime.now(),
        type="tweet",
        topic_match=rd.randint(1, 100)
    )


def home(request):
    return render(request, "core/home.html")


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

        messages.success(request, "Configuration updated successfully!")

        return render(request, 'core/configuration.html')


def topic_overview(request):
    topics = [get_random_topic() for _ in range(50)]

    return render(request, "core/topic_overview.html", dict(topics=topics))


def topic(request, id):
    current_topic = get_random_topic()
    documents = sorted([get_random_document() for _ in range(20)], key=lambda x: x.topic_match, reverse=True)

    return render(request, "core/topic.html", dict(topic=current_topic, documents=documents))
