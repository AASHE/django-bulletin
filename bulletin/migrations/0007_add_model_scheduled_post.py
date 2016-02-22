# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bulletin', '0006_add_post_field_cloned_from'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduledPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pub_date', models.DateField()),
                ('post', models.ForeignKey(to='bulletin.Post')),
            ],
        ),
    ]
