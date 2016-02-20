# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bulletin', '0005_delete_post_field_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='cloned_from',
            field=models.ForeignKey(blank=True, to='bulletin.Post', null=True),
        ),
    ]
