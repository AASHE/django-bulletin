# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bulletin', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('post_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='bulletin.Post')),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField(null=True, blank=True)),
                ('time', models.CharField(max_length=255, null=True, blank=True)),
                ('organization', models.CharField(max_length=255, null=True, blank=True)),
                ('location', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
            bases=('bulletin.post',),
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('post_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='bulletin.Post')),
                ('organization', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
            bases=('bulletin.post',),
        ),
        migrations.CreateModel(
            name='NewResource',
            fields=[
                ('post_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='bulletin.Post')),
                ('blurb', models.TextField()),
            ],
            options={
                'abstract': False,
            },
            bases=('bulletin.post',),
        ),
        migrations.CreateModel(
            name='Opportunity',
            fields=[
                ('post_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='bulletin.Post')),
                ('blurb', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'opportunities',
            },
            bases=('bulletin.post',),
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('post_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='bulletin.Post')),
                ('blurb', models.TextField()),
                ('date', models.DateTimeField()),
            ],
            options={
                'verbose_name_plural': 'stories',
            },
            bases=('bulletin.post',),
        ),
    ]
