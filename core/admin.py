from django.contrib import admin
from .models import *
admin.site.register(DocumentInTopic)
admin.site.register(Topic)
admin.site.register(Document)
admin.site.register(OriginalTopicProbabilities)
admin.site.register(TopicModel)
