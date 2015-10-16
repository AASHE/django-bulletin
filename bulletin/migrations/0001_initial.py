# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings
import positions.fields


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('django_constant_contact', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('start', models.DateField(null=True, blank=True)),
                ('end', models.DateField(null=True, blank=True)),
                ('url', models.URLField(max_length=255)),
                ('image', models.ImageField(max_length=512, null=True, upload_to=b'django-bulletin/%Y/%m/%d/ad', blank=True)),
                ('show_on_website', models.BooleanField(default=False)),
                ('include_in_newsletter', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='AdSize',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('height', models.PositiveSmallIntegerField()),
                ('width', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('fully_qualified_name', models.CharField(max_length=1024, null=True, blank=True)),
                ('private', models.BooleanField(default=False)),
                ('image', models.ImageField(max_length=512, null=True, upload_to=b'django-bulletin/%Y/%m/%d/category', blank=True)),
                ('url', models.URLField(max_length=640, null=True, blank=True)),
                ('parent', models.ForeignKey(blank=True, to='bulletin.Category', null=True)),
            ],
            options={
                'ordering': ['fully_qualified_name'],
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pub_date', models.DateField(null=True, blank=True)),
                ('html_template_name', models.CharField(max_length=1024, null=True, blank=True)),
                ('text_template_name', models.CharField(max_length=1024, null=True, blank=True)),
                ('introduction', models.TextField(null=True, blank=True)),
                ('name', models.CharField(max_length=128)),
                ('subject', models.CharField(max_length=128, null=True)),
                ('from_name', models.CharField(max_length=128, null=True)),
                ('from_email', models.EmailField(max_length=254, null=True)),
                ('reply_to_email', models.EmailField(max_length=254, null=True)),
                ('organization_name', models.CharField(max_length=128, null=True)),
                ('address_line_1', models.CharField(max_length=128, null=True)),
                ('address_line_2', models.CharField(max_length=128, null=True, blank=True)),
                ('address_line_3', models.CharField(max_length=128, null=True, blank=True)),
                ('city', models.CharField(max_length=128, null=True)),
                ('state', models.CharField(max_length=128, null=True)),
                ('international_state', models.CharField(max_length=128, null=True, blank=True)),
                ('postal_code', models.CharField(max_length=128, null=True)),
                ('country', models.CharField(max_length=128, null=True)),
                ('email_marketing_campaign', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, blank=True, to='django_constant_contact.EmailMarketingCampaign')),
            ],
            options={
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='IssueTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('subject', models.CharField(max_length=128, null=True, blank=True)),
                ('from_name', models.CharField(max_length=128, null=True, blank=True)),
                ('from_email', models.EmailField(max_length=254, null=True, blank=True)),
                ('reply_to_email', models.EmailField(max_length=254, null=True, blank=True)),
                ('organization_name', models.CharField(max_length=128, null=True, blank=True)),
                ('address_line_1', models.CharField(max_length=128, null=True, blank=True)),
                ('address_line_2', models.CharField(max_length=128, null=True, blank=True)),
                ('address_line_3', models.CharField(max_length=128, null=True, blank=True)),
                ('city', models.CharField(max_length=128, null=True, blank=True)),
                ('state', models.CharField(max_length=128, null=True, blank=True)),
                ('international_state', models.CharField(max_length=128, null=True, blank=True)),
                ('postal_code', models.CharField(max_length=128, null=True, blank=True)),
                ('country', models.CharField(max_length=128, null=True, blank=True)),
                ('html_template_name', models.CharField(max_length=1024, null=True, blank=True)),
                ('text_template_name', models.CharField(max_length=1024, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField(max_length=1024)),
                ('text', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=255)),
                ('mailing_list', models.CharField(max_length=255, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_submitted', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=255)),
                ('url', models.URLField(max_length=255)),
                ('approved', models.NullBooleanField()),
                ('include_in_newsletter', models.BooleanField(default=True)),
                ('feature', models.BooleanField(default=False)),
                ('pub_date', models.DateTimeField(null=True, blank=True)),
                ('position', models.IntegerField(null=True, blank=True)),
                ('image', models.ImageField(max_length=512, null=True, upload_to=b'django-bulletin/%Y/%m/%d/post', blank=True)),
                ('category', models.ForeignKey(related_name='posts', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='bulletin.Category', null=True)),
                ('polymorphic_ctype', models.ForeignKey(related_name='polymorphic_bulletin.post_set+', editable=False, to='contenttypes.ContentType', null=True)),
            ],
            options={
                'ordering': ('section', 'position'),
            },
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('position', models.IntegerField(null=True, blank=True)),
                ('categories', models.ManyToManyField(related_name='sections', null=True, to='bulletin.Category', blank=True)),
                ('content_types', models.ManyToManyField(to='contenttypes.ContentType', null=True, blank=True)),
                ('issue', models.ForeignKey(related_name='sections', to='bulletin.Issue')),
            ],
            options={
                'ordering': ('issue', 'position'),
            },
        ),
        migrations.CreateModel(
            name='SectionTemplate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('position', positions.fields.PositionField(default=-1, blank=True)),
                ('categories', models.ManyToManyField(related_name='section_templates', null=True, to='bulletin.Category', blank=True)),
                ('content_types', models.ManyToManyField(to='contenttypes.ContentType', null=True, blank=True)),
                ('issue_template', models.ForeignKey(related_name='section_templates', to='bulletin.IssueTemplate')),
            ],
            options={
                'ordering': ('issue_template', 'position'),
            },
        ),
        migrations.AddField(
            model_name='post',
            name='section',
            field=models.ForeignKey(related_name='posts', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='bulletin.Section', null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='submitter',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='link',
            name='post',
            field=models.ForeignKey(related_name='links', blank=True, to='bulletin.Post'),
        ),
        migrations.AddField(
            model_name='issuetemplate',
            name='newsletter',
            field=models.ForeignKey(related_name='issue_templates', blank=True, to='bulletin.Newsletter'),
        ),
        migrations.AddField(
            model_name='issue',
            name='newsletter',
            field=models.ForeignKey(related_name='issues', to='bulletin.Newsletter'),
        ),
        migrations.AddField(
            model_name='ad',
            name='size',
            field=models.ForeignKey(to='bulletin.AdSize'),
        ),
        migrations.AlterUniqueTogether(
            name='section',
            unique_together=set([('issue', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together=set([('parent', 'name')]),
        ),
    ]
