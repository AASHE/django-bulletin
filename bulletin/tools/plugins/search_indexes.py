import datetime

from haystack import indexes

import models


class EventIndex(indexes.SearchIndex,
                 indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    pub_date = indexes.DateTimeField(model_attr='pub_date', null=True)

    def get_model(self):
        return models.Event

    def index_queryset(self, **kwargs):
        return models.Event.objects.filter(approved=True,
                                           pub_date__lte=datetime.date.today())


class JobIndex(indexes.SearchIndex,
               indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    pub_date = indexes.DateTimeField(model_attr='pub_date', null=True)

    def get_model(self):
        return models.Job

    def index_queryset(self, **kwargs):
        return models.Job.objects.filter(approved=True,
                                         pub_date__lte=datetime.date.today())


class NewResourceIndex(indexes.SearchIndex,
                       indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    pub_date = indexes.DateTimeField(model_attr='pub_date', null=True)

    def get_model(self):
        return models.NewResource

    def index_queryset(self, **kwargs):
        return models.NewResource.objects.filter(
            approved=True,
            pub_date__lte=datetime.date.today())


class OpportunityIndex(indexes.SearchIndex,
                       indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    pub_date = indexes.DateTimeField(model_attr='pub_date', null=True)

    def get_model(self):
        return models.Opportunity

    def index_queryset(self, **kwargs):
        return models.Opportunity.objects.filter(
            approved=True,
            pub_date__lte=datetime.date.today())


class StoryIndex(indexes.SearchIndex,
                 indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    pub_date = indexes.DateTimeField(model_attr='pub_date', null=True)

    def get_model(self):
        return models.Story

    def index_queryset(self, **kwargs):
        return models.Story.objects.filter(approved=True,
                                           pub_date__lte=datetime.date.today())
