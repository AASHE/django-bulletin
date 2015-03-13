# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Event'
        db.create_table(u'plugins_event', (
            (u'post_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bulletin.Post'], unique=True, primary_key=True)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('time', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('organization', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'plugins', ['Event'])

        # Adding model 'Job'
        db.create_table(u'plugins_job', (
            (u'post_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bulletin.Post'], unique=True, primary_key=True)),
            ('organization', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'plugins', ['Job'])

        # Adding model 'NewResource'
        db.create_table(u'plugins_newresource', (
            (u'post_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bulletin.Post'], unique=True, primary_key=True)),
            ('blurb', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'plugins', ['NewResource'])

        # Adding model 'Opportunity'
        db.create_table(u'plugins_opportunity', (
            (u'post_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bulletin.Post'], unique=True, primary_key=True)),
            ('blurb', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'plugins', ['Opportunity'])

        # Adding model 'Story'
        db.create_table(u'plugins_story', (
            (u'post_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['bulletin.Post'], unique=True, primary_key=True)),
            ('blurb', self.gf('django.db.models.fields.TextField')()),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'plugins', ['Story'])


    def backwards(self, orm):
        # Deleting model 'Event'
        db.delete_table(u'plugins_event')

        # Deleting model 'Job'
        db.delete_table(u'plugins_job')

        # Deleting model 'NewResource'
        db.delete_table(u'plugins_newresource')

        # Deleting model 'Opportunity'
        db.delete_table(u'plugins_opportunity')

        # Deleting model 'Story'
        db.delete_table(u'plugins_story')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'bulletin.category': {
            'Meta': {'ordering': "['fully_qualified_name']", 'unique_together': "(('parent', 'name'),)", 'object_name': 'Category'},
            'fully_qualified_name': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bulletin.Category']", 'null': 'True', 'blank': 'True'})
        },
        u'bulletin.issue': {
            'Meta': {'ordering': "('-pub_date',)", 'object_name': 'Issue'},
            'address_line_1': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'address_line_2': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'address_line_3': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'email_marketing_campaign': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['django_constant_contact.EmailMarketingCampaign']", 'unique': 'True', 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'from_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True'}),
            'from_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'html_template_name': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'international_state': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'introduction': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'newsletter': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'issues'", 'to': u"orm['bulletin.Newsletter']"}),
            'organization_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'pub_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'reply_to_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'text_template_name': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'})
        },
        u'bulletin.newsletter': {
            'Meta': {'object_name': 'Newsletter'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mailing_list': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'bulletin.post': {
            'Meta': {'ordering': "('section', 'position')", 'object_name': 'Post'},
            'approved': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'posts'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['bulletin.Category']"}),
            'date_submitted': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'include_in_newsletter': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'polymorphic_ctype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'polymorphic_bulletin.post_set'", 'null': 'True', 'to': u"orm['contenttypes.ContentType']"}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '-1', 'null': 'True', 'blank': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'posts'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['bulletin.Section']"}),
            'submitter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255'})
        },
        u'bulletin.section': {
            'Meta': {'ordering': "('issue', 'position')", 'unique_together': "(('issue', 'name'),)", 'object_name': 'Section'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'sections'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['bulletin.Category']"}),
            'content_types': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sections'", 'to': u"orm['bulletin.Issue']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '-1'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'django_constant_contact.emailmarketingcampaign': {
            'Meta': {'object_name': 'EmailMarketingCampaign'},
            'constant_contact_id': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'data': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'plugins.event': {
            'Meta': {'ordering': "('section', 'position')", 'object_name': 'Event', '_ormbases': [u'bulletin.Post']},
            'end_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'post_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['bulletin.Post']", 'unique': 'True', 'primary_key': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'time': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'plugins.job': {
            'Meta': {'ordering': "('section', 'position')", 'object_name': 'Job', '_ormbases': [u'bulletin.Post']},
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'post_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['bulletin.Post']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'plugins.newresource': {
            'Meta': {'ordering': "('section', 'position')", 'object_name': 'NewResource', '_ormbases': [u'bulletin.Post']},
            'blurb': ('django.db.models.fields.TextField', [], {}),
            u'post_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['bulletin.Post']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'plugins.opportunity': {
            'Meta': {'ordering': "('section', 'position')", 'object_name': 'Opportunity', '_ormbases': [u'bulletin.Post']},
            'blurb': ('django.db.models.fields.TextField', [], {}),
            u'post_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['bulletin.Post']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'plugins.story': {
            'Meta': {'ordering': "('section', 'position')", 'object_name': 'Story', '_ormbases': [u'bulletin.Post']},
            'blurb': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            u'post_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['bulletin.Post']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['plugins']