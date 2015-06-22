from haystack import indexes
import models


class ApprovedIndexMixin(object):


    def index_queryset(self, **kwargs):
        return self.get_model().objects.filter(approved=True)


class EventIndex(indexes.SearchIndex,
                 indexes.Indexable,
                 ApprovedIndexMixin):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return models.Event


class JobIndex(indexes.SearchIndex,
               indexes.Indexable,
               ApprovedIndexMixin):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return models.Job


class NewResourceIndex(indexes.SearchIndex,
                       indexes.Indexable,
                       ApprovedIndexMixin):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return models.NewResource


class OpportunityIndex(indexes.SearchIndex,
                       indexes.Indexable,
                       ApprovedIndexMixin):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return models.Opportunity


class StoryIndex(indexes.SearchIndex,
                 indexes.Indexable,
                 ApprovedIndexMixin):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return models.Story
