# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bulletin', '0008_ad_display_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='display_weight',
            field=models.SmallIntegerField(default=1, help_text=b'Ads appear in ascending order of Display Weight', db_index=True),
        ),
        migrations.AlterField(
            model_name='ad',
            name='end',
            field=models.DateField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='ad',
            name='include_in_newsletter',
            field=models.BooleanField(default=False, db_index=True),
        ),
        migrations.AlterField(
            model_name='ad',
            name='show_on_website',
            field=models.BooleanField(default=False, db_index=True),
        ),
        migrations.AlterField(
            model_name='ad',
            name='start',
            field=models.DateField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='fully_qualified_name',
            field=models.CharField(db_index=True, max_length=1024, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=255, db_index=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='pub_date',
            field=models.DateField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='approved',
            field=models.NullBooleanField(db_index=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='date_submitted',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='feature',
            field=models.BooleanField(default=False, db_index=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='include_in_newsletter',
            field=models.BooleanField(default=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='position',
            field=models.IntegerField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='pub_date',
            field=models.DateTimeField(db_index=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='scheduledpost',
            name='pub_date',
            field=models.DateField(db_index=True),
        ),
        migrations.AlterField(
            model_name='section',
            name='name',
            field=models.CharField(max_length=255, db_index=True),
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together=set([]),
        ),
        migrations.AlterUniqueTogether(
            name='postcategory',
            unique_together=set([]),
        ),
        migrations.AlterUniqueTogether(
            name='section',
            unique_together=set([]),
        ),
        migrations.AlterIndexTogether(
            name='category',
            index_together=set([('parent', 'name')]),
        ),
        migrations.AlterIndexTogether(
            name='postcategory',
            index_together=set([('post', 'category')]),
        ),
        migrations.AlterIndexTogether(
            name='section',
            index_together=set([('issue', 'position')]),
        ),
        migrations.AlterIndexTogether(
            name='sectiontemplate',
            index_together=set([('issue_template', 'position')]),
        ),
    ]
