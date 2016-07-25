# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bulletin', '0007_add_model_scheduled_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='ad',
            name='display_weight',
            field=models.SmallIntegerField(default=1, help_text=b'Ads appear in ascending order of Display Weight'),
        ),
    ]
