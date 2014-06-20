# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Quests.size'
        db.add_column(u'quests_quests', 'size',
                      self.gf('django.db.models.fields.TextField')(default='backpack'),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Quests.size'
        db.delete_column(u'quests_quests', 'size')


    models = {
        u'quests.questcomments': {
            'Meta': {'object_name': 'QuestComments'},
            'comment': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quest': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['quests.Quests']"}),
            'questr': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.QuestrUserProfile']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'quests.quests': {
            'Meta': {'object_name': 'Quests'},
            'creation_date': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'dstaddress': ('django.db.models.fields.TextField', [], {}),
            'dstcity': ('django.db.models.fields.TextField', [], {'default': "'Toronto'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isaccepted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'item_images': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'questrs': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.QuestrUserProfile']"}),
            'reward': ('django.db.models.fields.DecimalField', [], {'max_digits': '1000', 'decimal_places': '2'}),
            'size': ('django.db.models.fields.TextField', [], {'default': "'backpack'"}),
            'srcaddress': ('django.db.models.fields.TextField', [], {}),
            'srccity': ('django.db.models.fields.TextField', [], {'default': "'Toronto'"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': "'0'"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'users.questruserprofile': {
            'Meta': {'object_name': 'QuestrUserProfile'},
            'account_status': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '1', 'blank': 'True'}),
            'avatar_file_name': ('django.db.models.fields.files.ImageField', [], {'max_length': '9999'}),
            'biography': ('django.db.models.fields.TextField', [], {'max_length': '9999', 'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'displayname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '100'}),
            'email_status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'privacy': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['quests']