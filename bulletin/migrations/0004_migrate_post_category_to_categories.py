# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def migrate_categories(apps, schema_editor):
    Post = apps.get_model("bulletin", "Post")
    PostCategory = apps.get_model("bulletin", "PostCategory")
    for post in Post.objects.filter(category__isnull=False):
        PostCategory.objects.create(post=post,
                                    category=post.category,
                                    primary=True)


class Migration(migrations.Migration):

    dependencies = [
        ('bulletin', '0003_add_field_post_categories'),
    ]

    operations = [
        migrations.RunPython(migrate_categories)
    ]
