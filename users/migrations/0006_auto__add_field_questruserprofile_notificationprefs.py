# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'QuestrUserProfile.notificationprefs'
        db.add_column(u'users_questruserprofile', 'notificationprefs',
                      self.gf('django.db.models.fields.CharField')(default='{}', max_length=9999),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'QuestrUserProfile.notificationprefs'
        db.delete_column(u'users_questruserprofile', 'notificationprefs')


    models = {
        u'users.questrtoken': {
            'Meta': {'object_name': 'QuestrToken'},
            'timeframe': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'token_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'})
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
        },
        u'users.usertransactional': {
            'Meta': {'object_name': 'UserTransactional'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        }
    }

    complete_apps = ['users']