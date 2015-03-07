# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'QuestPricing'
        db.delete_table(u'quests_questpricing')


    def backwards(self, orm):
        # Adding model 'QuestPricing'
        db.create_table(u'quests_questpricing', (
            ('updated_on', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('questrs', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.QuestrUserProfile'], unique=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pricing', self.gf('jsonfield.fields.JSONField')(default={})),
        ))
        db.send_create_signal(u'quests', ['QuestPricing'])


    models = {
        u'quests.questcomments': {
            'Meta': {'object_name': 'QuestComments'},
            'comment': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quest': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['quests.Quests']"}),
            'questr': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.QuestrUserProfile']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'quests.questevents': {
            'Meta': {'object_name': 'QuestEvents'},
            'event': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '2'}),
            'extrainfo': ('jsonfield.fields.JSONField', [], {'default': "'{}'", 'max_length': '9999'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quest': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['quests.Quests']"}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        u'quests.quests': {
            'Meta': {'object_name': 'Quests'},
            'available_couriers': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'considered_couriers': ('django.db.models.fields.TextField', [], {'default': '[]'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'delivery_code': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'delivery_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'distance': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '1000', 'decimal_places': '2'}),
            'dropoff': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_complete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_questr_reviewed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_shipper_reviewed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'isaccepted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ishidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'isnotified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'item_images': ('django.db.models.fields.files.ImageField', [], {'max_length': '9999', 'blank': 'True'}),
            'map_image': ('django.db.models.fields.URLField', [], {'default': "''", 'max_length': '9999'}),
            'pickup': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'pickup_time': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'questrs': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'quests'", 'to': u"orm['users.QuestrUserProfile']"}),
            'reward': ('django.db.models.fields.DecimalField', [], {'max_digits': '1000', 'decimal_places': '2'}),
            'shipper': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'size': ('django.db.models.fields.TextField', [], {'default': "'backpack'"}),
            'status': ('django.db.models.fields.TextField', [], {'default': "'New'"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'tracking_number': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'quests.questtoken': {
            'Meta': {'object_name': 'QuestToken'},
            'timeframe': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'token_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'})
        },
        u'quests.questtransactional': {
            'Meta': {'object_name': 'QuestTransactional'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quest': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['quests.Quests']"}),
            'quest_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'shipper': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['users.QuestrUserProfile']"}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'transaction_type': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        u'users.questruserprofile': {
            'Meta': {'object_name': 'QuestrUserProfile'},
            'account_status': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '1', 'blank': 'True'}),
            'address': ('jsonfield.fields.JSONField', [], {'default': "'{}'", 'max_length': '9999'}),
            'avatar': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '1024', 'blank': 'True'}),
            'biography': ('django.db.models.fields.TextField', [], {'max_length': '9999', 'blank': 'True'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'displayname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '100'}),
            'email_status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_available': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_shipper': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'notificationprefs': ('jsonfield.fields.JSONField', [], {'default': "'{}'", 'max_length': '9999'}),
            'notifications': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'privacy': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rating': ('django.db.models.fields.DecimalField', [], {'default': "'0'", 'max_digits': '5', 'decimal_places': '2'}),
            'vehicle': ('django.db.models.fields.CharField', [], {'default': "'car'", 'max_length': '10', 'blank': 'True'})
        }
    }

    complete_apps = ['quests']