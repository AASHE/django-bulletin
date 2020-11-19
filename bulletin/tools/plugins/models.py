from django.db import models

from bulletin.models import Post


class Event(Post):

    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    time = models.CharField(max_length=255,
                            null=True, blank=True)
    organization = models.CharField(max_length=255,
                                    null=True, blank=True)
    location = models.CharField(max_length=255)

    def clone(self):
        new_event = Event()
        new_event.start_date = self.start_date
        new_event.end_date = self.end_date
        new_event.time = self.time
        new_event.organization = self.organization
        new_event.location = self.location
        new_event = super(Event, self).clone(new_event)
        return new_event


class Job(Post):

    organization = models.CharField(max_length=255)

    def clone(self):
        new_job = Job()
        new_job.organization = self.organization
        new_job = super(Job, self).clone(new_job)
        return new_job


class NewResource(Post):

    blurb = models.TextField()
    verbose_name = 'newresource'

    def clone(self):
        new_new_resource = NewResource()
        new_new_resource.blurb = self.blurb
        new_new_resource = super(NewResource, self).clone(new_new_resource)
        return new_new_resource


class Opportunity(Post):

    blurb = models.TextField()

    class Meta:
        verbose_name_plural = 'opportunities'

    def clone(self):
        new_opportunity = Opportunity()
        new_opportunity.blurb = self.blurb
        new_opportunity = super(Opportunity, self).clone(new_opportunity)
        return new_opportunity


class Story(Post):

    blurb = models.TextField(required=False)
    date = models.DateTimeField()

    class Meta:
        verbose_name_plural = 'stories'

    def clone(self):
        new_story = Story()
        new_story.blurb = self.blurb
        new_story.date = self.date
        new_story = super(Story, self).clone(new_story)
        return new_story
