# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SMS'
        db.create_table(u'sms_sms', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mobile_number', self.gf('django.db.models.fields.CharField')(max_length=12)),
            ('delivery_status', self.gf('django.db.models.fields.CharField')(default='unknown', max_length=16)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('message_id', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=32, null=True, blank=True)),
        ))
        db.send_create_signal(u'sms', ['SMS'])


    def backwards(self, orm):
        # Deleting model 'SMS'
        db.delete_table(u'sms_sms')


    models = {
        u'sms.sms': {
            'Meta': {'object_name': 'SMS'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'delivery_status': ('django.db.models.fields.CharField', [], {'default': "'unknown'", 'max_length': '16'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'mobile_number': ('django.db.models.fields.CharField', [], {'max_length': '12'})
        }
    }

    complete_apps = ['sms']