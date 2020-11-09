from django.shortcuts import render
from .models import *
import datetime


def get_random_document():
    return Document(
        url="https://twist.com/a/131368/ch/391926/t/1996519/",
        doi="https://doi.org/10.1257/aer.101.3.318",
        title="Trusted Decision-Making: Data Governance for Creating Trust in Data Science Decision Outcomes",
        text="Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.",
        date=datetime.datetime.now(),
        type="tweet"
    )


def home(request):
    return render(request, "core/home.html")


def topic(request, id):
    current_topic = Topic(name="XYZ",
                          description="Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.")

    documents = [get_random_document() for _ in range(20)]

    return render(request, "core/topic.html", dict(topic=current_topic, documents=documents))
