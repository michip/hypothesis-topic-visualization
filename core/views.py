from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404
from .models import *
import datetime
import random as rd
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required

from .statistics import TopicStatistic


def home(request):
    return render(request, "core/home.html", dict(
        topics=Topic.objects.all().annotate(length=Count('documents')).order_by('-length'), document_count=Document.objects.count()))


def search(request):
    context = dict(topics=Topic.objects.all(), types=Document.TYPE_CHOICES,
                   form=dict(query="", topics=[]))

    if request.method == "GET":
        query = str(request.GET.get("query", ""))
        page_number = request.GET.get('page')

        topics = [int(k) for k in request.GET.getlist("topics")]
        types = [str(k) for k in request.GET.getlist("types")]

        documents = Document.objects.all()

        if topics:
            documents = documents.filter(topics__pk__in=topics)

        if types:
            documents = documents.filter(document_type__in=types)

        if query:

            filter_query = Q()
            for word in query.lower().split():
                filter_query |= Q(title__icontains=word)

            documents = documents.filter(filter_query)

        paginator = Paginator(documents, 10)

        try:
            page_obj = paginator.get_page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        context["documents"] = page_obj
        context["form"]["query"] = query
        context["form"]["topics"] = topics
        context["form"]["types"] = types

        return render(request, "core/search.html", context)

@login_required
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
                    document_in_topic = DocumentInTopic(document=doc,
                                                        topic=orig_prob.topic, probability=orig_prob.probability)
                    document_in_topic.save()
                    current_value += orig_prob.probability

        messages.success(request, "Configuration updated successfully!")

        return render(request, 'core/configuration.html')


def topic_overview(request):
    return render(request, "core/topic_overview.html",
                  dict(topics=Topic.objects.all().annotate(length=Count('documents')).order_by('-length')))


def topic(request, id):
    current_topic = get_object_or_404(Topic, pk=id)

    statistics = TopicStatistic(topic=current_topic)

    paginator = Paginator(DocumentInTopic.objects.filter(topic=current_topic).order_by("-probability"), 10)
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, "core/topic.html", dict(topic=current_topic,
                                                   documents_in_topic=page_obj,
                                                   statistics=statistics))
