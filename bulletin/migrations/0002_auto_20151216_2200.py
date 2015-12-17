# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bulletin', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='url',
            field=models.URLField(max_length=1024),
        ),
        migrations.AlterField(
            model_name='category',
            name='url',
            field=models.URLField(max_length=1024, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='url',
            field=models.URLField(max_length=1024),
        ),
        migrations.AlterField(
            model_name='section',
            name='categories',
            field=models.ManyToManyField(related_name='sections', to='bulletin.Category', blank=True),
        ),
        migrations.AlterField(
            model_name='section',
            name='content_types',
            field=models.ManyToManyField(to='contenttypes.ContentType', blank=True),
        ),
        migrations.AlterField(
            model_name='sectiontemplate',
            name='categories',
            field=models.ManyToManyField(related_name='section_templates', to='bulletin.Category', blank=True),
        ),
        migrations.AlterField(
            model_name='sectiontemplate',
            name='content_types',
            field=models.ManyToManyField(to='contenttypes.ContentType', blank=True),
        ),
    ]
