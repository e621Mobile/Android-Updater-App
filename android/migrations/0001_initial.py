# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AndroidApp'
        db.create_table(u'android_androidapp', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('app_id', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal(u'android', ['AndroidApp'])

        # Adding model 'AppVersion'
        db.create_table(u'android_appversion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('apk', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('local_id', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('version_name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['android.AndroidApp'])),
        ))
        db.send_create_signal(u'android', ['AppVersion'])

        # Adding unique constraint on 'AppVersion', fields ['app', 'local_id']
        db.create_unique(u'android_appversion', ['app_id', 'local_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'AppVersion', fields ['app', 'local_id']
        db.delete_unique(u'android_appversion', ['app_id', 'local_id'])

        # Deleting model 'AndroidApp'
        db.delete_table(u'android_androidapp')

        # Deleting model 'AppVersion'
        db.delete_table(u'android_appversion')


    models = {
        u'android.androidapp': {
            'Meta': {'object_name': 'AndroidApp'},
            'app_id': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'android.appversion': {
            'Meta': {'unique_together': "(('app', 'local_id'),)", 'object_name': 'AppVersion'},
            'apk': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['android.AndroidApp']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local_id': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'version_name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        }
    }

    complete_apps = ['android']