# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bulletin', '0004_migrate_post_category_to_categories'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='postcategory',
            options={'ordering': ('post', '-primary')},
        ),
        migrations.RemoveField(
            model_name='post',
            name='category',
        ),
        migrations.AlterField(
            model_name='post',
            name='categories',
            field=models.ManyToManyField(related_name='posts',
                                         through='bulletin.PostCategory',
                                         to='bulletin.Category',
                                         blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='postcategory',
            unique_together=set([('post', 'category')]),
        ),
    ]
