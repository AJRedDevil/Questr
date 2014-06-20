# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'QuestrUserProfile'
        db.create_table(u'users_questruserprofile', (
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('displayname', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=100)),
            ('email_status', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=15, blank=True)),
            ('date_joined', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('avatar_file_name', self.gf('django.db.models.fields.files.ImageField')(max_length=9999)),
            ('biography', self.gf('django.db.models.fields.TextField')(max_length=9999, blank=True)),
            ('account_status', self.gf('django.db.models.fields.IntegerField')(default=1, max_length=1, blank=True)),
            ('privacy', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'users', ['QuestrUserProfile'])

        # Adding model 'UserTransactional'
        db.create_table(u'users_usertransactional', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('user_code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=100)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'users', ['UserTransactional'])

        # Adding model 'QuestrToken'
        db.create_table(u'users_questrtoken', (
            ('token_id', self.gf('django.db.models.fields.CharField')(max_length=20, primary_key=True)),
            ('timeframe', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'users', ['QuestrToken'])


    def backwards(self, orm):
        # Deleting model 'QuestrUserProfile'
        db.delete_table(u'users_questruserprofile')

        # Deleting model 'UserTransactional'
        db.delete_table(u'users_usertransactional')

        # Deleting model 'QuestrToken'
        db.delete_table(u'users_questrtoken')


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
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'privacy': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'users.usertransactional': {
            'Meta': {'object_name': 'UserTransactional'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '100'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        }
    }

    complete_apps = ['users']