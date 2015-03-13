# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Newsletter'
        db.create_table(u'bulletin_newsletter', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('mailing_list', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'bulletin', ['Newsletter'])

        # Adding model 'Issue'
        db.create_table(u'bulletin_issue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('newsletter', self.gf('django.db.models.fields.related.ForeignKey')(related_name='issues', to=orm['bulletin.Newsletter'])),
            ('pub_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('html_template_name', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
            ('text_template_name', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
            ('email_marketing_campaign', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['django_constant_contact.EmailMarketingCampaign'], unique=True, null=True, on_delete=models.SET_NULL, blank=True)),
            ('introduction', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=128, null=True)),
            ('from_name', self.gf('django.db.models.fields.CharField')(max_length=128, null=True)),
            ('from_email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True)),
            ('reply_to_email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True)),
            ('organization_name', self.gf('django.db.models.fields.CharField')(max_length=128, null=True)),
            ('address_line_1', self.gf('django.db.models.fields.CharField')(max_length=128, null=True)),
            ('address_line_2', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('address_line_3', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=128, null=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=128, null=True)),
            ('international_state', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('postal_code', self.gf('django.db.models.fields.CharField')(max_length=128, null=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=128, null=True)),
        ))
        db.send_create_signal(u'bulletin', ['Issue'])

        # Adding model 'Category'
        db.create_table(u'bulletin_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bulletin.Category'], null=True, blank=True)),
            ('fully_qualified_name', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=512, null=True, blank=True)),
        ))
        db.send_create_signal(u'bulletin', ['Category'])

        # Adding unique constraint on 'Category', fields ['parent', 'name']
        db.create_unique(u'bulletin_category', ['parent_id', 'name'])

        # Adding model 'Section'
        db.create_table(u'bulletin_section', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('issue', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sections', to=orm['bulletin.Issue'])),
            ('position', self.gf('django.db.models.fields.IntegerField')(default=-1)),
        ))
        db.send_create_signal(u'bulletin', ['Section'])

        # Adding unique constraint on 'Section', fields ['issue', 'name']
        db.create_unique(u'bulletin_section', ['issue_id', 'name'])

        # Adding M2M table for field categories on 'Section'
        m2m_table_name = db.shorten_name(u'bulletin_section_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('section', models.ForeignKey(orm[u'bulletin.section'], null=False)),
            ('category', models.ForeignKey(orm[u'bulletin.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['section_id', 'category_id'])

        # Adding M2M table for field content_types on 'Section'
        m2m_table_name = db.shorten_name(u'bulletin_section_content_types')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('section', models.ForeignKey(orm[u'bulletin.section'], null=False)),
            ('contenttype', models.ForeignKey(orm[u'contenttypes.contenttype'], null=False))
        ))
        db.create_unique(m2m_table_name, ['section_id', 'contenttype_id'])

        # Adding model 'Post'
        db.create_table(u'bulletin_post', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('polymorphic_ctype', self.gf('django.db.models.fields.related.ForeignKey')(related_name=u'polymorphic_bulletin.post_set', null=True, to=orm['contenttypes.ContentType'])),
            ('date_submitted', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=255)),
            ('submitter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('approved', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('include_in_newsletter', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='posts', null=True, on_delete=models.SET_NULL, to=orm['bulletin.Category'])),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='posts', null=True, on_delete=models.SET_NULL, to=orm['bulletin.Section'])),
            ('position', self.gf('django.db.models.fields.IntegerField')(default=-1, null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=512, null=True, blank=True)),
        ))
        db.send_create_signal(u'bulletin', ['Post'])

        # Adding model 'Link'
        db.create_table(u'bulletin_link', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=1024)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(related_name='links', blank=True, to=orm['bulletin.Post'])),
        ))
        db.send_create_signal(u'bulletin', ['Link'])

        # Adding model 'IssueTemplate'
        db.create_table(u'bulletin_issuetemplate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('newsletter', self.gf('django.db.models.fields.related.ForeignKey')(related_name='issue_templates', blank=True, to=orm['bulletin.Newsletter'])),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('from_name', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('from_email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('reply_to_email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('organization_name', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('address_line_1', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('address_line_2', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('address_line_3', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('international_state', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('postal_code', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('html_template_name', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
            ('text_template_name', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
        ))
        db.send_create_signal(u'bulletin', ['IssueTemplate'])

        # Adding model 'SectionTemplate'
        db.create_table(u'bulletin_sectiontemplate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('issue_template', self.gf('django.db.models.fields.related.ForeignKey')(related_name='section_templates', to=orm['bulletin.IssueTemplate'])),
            ('position', self.gf('django.db.models.fields.IntegerField')(default=-1, blank=True)),
        ))
        db.send_create_signal(u'bulletin', ['SectionTemplate'])

        # Adding M2M table for field categories on 'SectionTemplate'
        m2m_table_name = db.shorten_name(u'bulletin_sectiontemplate_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('sectiontemplate', models.ForeignKey(orm[u'bulletin.sectiontemplate'], null=False)),
            ('category', models.ForeignKey(orm[u'bulletin.category'], null=False))
        ))
        db.create_unique(m2m_table_name, ['sectiontemplate_id', 'category_id'])

        # Adding M2M table for field content_types on 'SectionTemplate'
        m2m_table_name = db.shorten_name(u'bulletin_sectiontemplate_content_types')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('sectiontemplate', models.ForeignKey(orm[u'bulletin.sectiontemplate'], null=False)),
            ('contenttype', models.ForeignKey(orm[u'contenttypes.contenttype'], null=False))
        ))
        db.create_unique(m2m_table_name, ['sectiontemplate_id', 'contenttype_id'])

        # Adding model 'AdSize'
        db.create_table(u'bulletin_adsize', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('height', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
            ('width', self.gf('django.db.models.fields.PositiveSmallIntegerField')()),
        ))
        db.send_create_signal(u'bulletin', ['AdSize'])

        # Adding model 'Ad'
        db.create_table(u'bulletin_ad', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('start', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('end', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('size', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bulletin.AdSize'])),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=255)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=512, null=True, blank=True)),
            ('show_on_website', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('include_in_newsletter', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'bulletin', ['Ad'])


    def backwards(self, orm):
        # Removing unique constraint on 'Section', fields ['issue', 'name']
        db.delete_unique(u'bulletin_section', ['issue_id', 'name'])

        # Removing unique constraint on 'Category', fields ['parent', 'name']
        db.delete_unique(u'bulletin_category', ['parent_id', 'name'])

        # Deleting model 'Newsletter'
        db.delete_table(u'bulletin_newsletter')

        # Deleting model 'Issue'
        db.delete_table(u'bulletin_issue')

        # Deleting model 'Category'
        db.delete_table(u'bulletin_category')

        # Deleting model 'Section'
        db.delete_table(u'bulletin_section')

        # Removing M2M table for field categories on 'Section'
        db.delete_table(db.shorten_name(u'bulletin_section_categories'))

        # Removing M2M table for field content_types on 'Section'
        db.delete_table(db.shorten_name(u'bulletin_section_content_types'))

        # Deleting model 'Post'
        db.delete_table(u'bulletin_post')

        # Deleting model 'Link'
        db.delete_table(u'bulletin_link')

        # Deleting model 'IssueTemplate'
        db.delete_table(u'bulletin_issuetemplate')

        # Deleting model 'SectionTemplate'
        db.delete_table(u'bulletin_sectiontemplate')

        # Removing M2M table for field categories on 'SectionTemplate'
        db.delete_table(db.shorten_name(u'bulletin_sectiontemplate_categories'))

        # Removing M2M table for field content_types on 'SectionTemplate'
        db.delete_table(db.shorten_name(u'bulletin_sectiontemplate_content_types'))

        # Deleting model 'AdSize'
        db.delete_table(u'bulletin_adsize')

        # Deleting model 'Ad'
        db.delete_table(u'bulletin_ad')


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
        u'bulletin.ad': {
            'Meta': {'object_name': 'Ad'},
            'end': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'include_in_newsletter': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'show_on_website': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'size': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bulletin.AdSize']"}),
            'start': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '255'})
        },
        u'bulletin.adsize': {
            'Meta': {'object_name': 'AdSize'},
            'height': ('django.db.models.fields.PositiveSmallIntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'width': ('django.db.models.fields.PositiveSmallIntegerField', [], {})
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
        u'bulletin.issuetemplate': {
            'Meta': {'object_name': 'IssueTemplate'},
            'address_line_1': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'address_line_2': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'address_line_3': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'from_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'from_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'html_template_name': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'international_state': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'newsletter': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'issue_templates'", 'blank': 'True', 'to': u"orm['bulletin.Newsletter']"}),
            'organization_name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'reply_to_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'text_template_name': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'})
        },
        u'bulletin.link': {
            'Meta': {'object_name': 'Link'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'links'", 'blank': 'True', 'to': u"orm['bulletin.Post']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '1024'})
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
        u'bulletin.sectiontemplate': {
            'Meta': {'ordering': "('issue_template', 'position')", 'object_name': 'SectionTemplate'},
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'section_templates'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['bulletin.Category']"}),
            'content_types': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue_template': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'section_templates'", 'to': u"orm['bulletin.IssueTemplate']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '-1', 'blank': 'True'})
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
        }
    }

    complete_apps = ['bulletin']