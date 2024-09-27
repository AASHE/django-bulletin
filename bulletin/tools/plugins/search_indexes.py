from django.utils import timezone
from haystack import indexes

from .models import *


class EventIndex(indexes.SearchIndex,
                 indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    pub_date = indexes.DateTimeField(model_attr='pub_date', null=True)

    def get_model(self):
        return Event

    def index_queryset(self, **kwargs):
        return Event.objects.filter(approved=True,
                                           pub_date__lte=timezone.now())


class JobIndex(indexes.SearchIndex,
               indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    pub_date = indexes.DateTimeField(model_attr='pub_date', null=True)

    def get_model(self):
        return Job

    def index_queryset(self, **kwargs):
        return Job.objects.filter(approved=True,
                                         pub_date__lte=timezone.now())


class NewResourceIndex(indexes.SearchIndex,
                       indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    pub_date = indexes.DateTimeField(model_attr='pub_date', null=True)

    def get_model(self):
        return NewResource

    def index_queryset(self, **kwargs):
        return NewResource.objects.filter(
            approved=True,
            pub_date__lte=timezone.now())


class OpportunityIndex(indexes.SearchIndex,
                       indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    pub_date = indexes.DateTimeField(model_attr='pub_date', null=True)

    def get_model(self):
        return Opportunity

    def index_queryset(self, **kwargs):
        return Opportunity.objects.filter(
            approved=True,
            pub_date__lte=timezone.now())


class StoryIndex(indexes.SearchIndex,
                 indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    pub_date = indexes.DateTimeField(model_attr='pub_date', null=True)

    def get_model(self):
        return Story

    def index_queryset(self, **kwargs):
        return Story.objects.filter(approved=True,
                                           pub_date__lte=timezone.now())
