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


class Job(Post):

    organization = models.CharField(max_length=255)


class NewResource(Post):

    blurb = models.TextField()
    verbose_name = 'newresource'


class Opportunity(Post):

    blurb = models.TextField()

    class Meta:
        verbose_name_plural = 'opportunities'


class Story(Post):

    blurb = models.TextField()
    date = models.DateTimeField()

    class Meta:
        verbose_name_plural = 'stories'
