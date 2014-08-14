# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Quests.srcaddress'
        db.delete_column(u'quests_quests', 'srcaddress')

        # Deleting field 'Quests.srccity'
        db.delete_column(u'quests_quests', 'srccity')

        # Deleting field 'Quests.dstaddress'
        db.delete_column(u'quests_quests', 'dstaddress')

        # Deleting field 'Quests.dstcity'
        db.delete_column(u'quests_quests', 'dstcity')

        # Adding field 'Quests.pickup'
        db.add_column(u'quests_quests', 'pickup',
                      self.gf('django.db.models.fields.TextField')(default={}),
                      keep_default=False)

        # Adding field 'Quests.dropoff'
        db.add_column(u'quests_quests', 'dropoff',
                      self.gf('django.db.models.fields.TextField')(default={}),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Quests.srcaddress'
        raise RuntimeError("Cannot reverse this migration. 'Quests.srcaddress' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Quests.srcaddress'
        db.add_column(u'quests_quests', 'srcaddress',
                      self.gf('django.db.models.fields.TextField')(),
                      keep_default=False)

        # Adding field 'Quests.srccity'
        db.add_column(u'quests_quests', 'srccity',
                      self.gf('django.db.models.fields.TextField')(default='Toronto'),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Quests.dstaddress'
        raise RuntimeError("Cannot reverse this migration. 'Quests.dstaddress' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Quests.dstaddress'
        db.add_column(u'quests_quests', 'dstaddress',
                      self.gf('django.db.models.fields.TextField')(),
                      keep_default=False)

        # Adding field 'Quests.dstcity'
        db.add_column(u'quests_quests', 'dstcity',
                      self.gf('django.db.models.fields.TextField')(default='Toronto'),
                      keep_default=False)

        # Deleting field 'Quests.pickup'
        db.delete_column(u'quests_quests', 'pickup')

        # Deleting field 'Quests.dropoff'
        db.delete_column(u'quests_quests', 'dropoff')


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
            'creation_date': ('django.db.models.fields.DateTimeField', [], {}),
            'delivery_code': ('django.db.models.fields.TextField', [], {'default': "'121212'"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'distance': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '1000', 'decimal_places': '2'}),
            'dropoff': ('django.db.models.fields.TextField', [], {'default': '{}'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_complete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_questr_reviewed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_shipper_reviewed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'isaccepted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ishidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'isnotified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'item_images': ('django.db.models.fields.files.ImageField', [], {'max_length': '9999', 'blank': 'True'}),
            'pickup': ('django.db.models.fields.TextField', [], {'default': '{}'}),
            'questrs': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.QuestrUserProfile']"}),
            'reward': ('django.db.models.fields.DecimalField', [], {'max_digits': '1000', 'decimal_places': '2'}),
            'shipper': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'size': ('django.db.models.fields.TextField', [], {'default': "'backpack'"}),
            'status': ('django.db.models.fields.TextField', [], {'default': "'new'"}),
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
            'is_shipper': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'notificationprefs': ('django.db.models.fields.CharField', [], {'default': "'{}'", 'max_length': '9999'}),
            'notifications': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'privacy': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rating': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'max_digits': '5', 'decimal_places': '2'})
        }
    }

    complete_apps = ['quests']