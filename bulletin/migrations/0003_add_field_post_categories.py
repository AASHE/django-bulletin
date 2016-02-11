# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bulletin', '0002_auto_20151216_2200'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID',
                                        serialize=False,
                                        auto_created=True,
                                        primary_key=True)),
                ('primary', models.BooleanField(default=False)),
                ('category', models.ForeignKey(to='bulletin.Category')),
                ('post', models.ForeignKey(to='bulletin.Post')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='categories',
            field=models.ManyToManyField(to='bulletin.Category',
                                         through='bulletin.PostCategory',
                                         blank=True),
        ),
    ]
