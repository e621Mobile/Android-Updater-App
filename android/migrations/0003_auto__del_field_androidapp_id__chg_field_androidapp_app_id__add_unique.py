# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'AndroidApp.id'
        db.delete_column(u'android_androidapp', u'id')


        # Changing field 'AndroidApp.app_id'
        db.alter_column(u'android_androidapp', 'app_id', self.gf('django.db.models.fields.CharField')(max_length=32, primary_key=True))
        # Adding unique constraint on 'AndroidApp', fields ['app_id']
        db.create_unique(u'android_androidapp', ['app_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'AndroidApp', fields ['app_id']
        db.delete_unique(u'android_androidapp', ['app_id'])


        # User chose to not deal with backwards NULL issues for 'AndroidApp.id'
        raise RuntimeError("Cannot reverse this migration. 'AndroidApp.id' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'AndroidApp.id'
        db.add_column(u'android_androidapp', u'id',
                      self.gf('django.db.models.fields.AutoField')(primary_key=True),
                      keep_default=False)


        # Changing field 'AndroidApp.app_id'
        db.alter_column(u'android_androidapp', 'app_id', self.gf('django.db.models.fields.CharField')(max_length=32))

    models = {
        u'RSS.user': {
            'Meta': {'object_name': 'User'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'preffered_currency': ('django.db.models.fields.IntegerField', [], {})
        },
        u'android.androidapp': {
            'Meta': {'object_name': 'AndroidApp'},
            'app_id': ('django.db.models.fields.CharField', [], {'max_length': '32', 'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['android.AndroidUser']"})
        },
        u'android.androiduser': {
            'Meta': {'object_name': 'AndroidUser'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['RSS.User']", 'unique': 'True'})
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