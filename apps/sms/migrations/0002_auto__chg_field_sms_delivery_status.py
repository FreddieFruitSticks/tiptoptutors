# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'SMS.delivery_status'
        db.alter_column(u'sms_sms', 'delivery_status', self.gf('django.db.models.fields.TextField')())

    def backwards(self, orm):

        # Changing field 'SMS.delivery_status'
        db.alter_column(u'sms_sms', 'delivery_status', self.gf('django.db.models.fields.CharField')(max_length=16))

    models = {
        u'sms.sms': {
            'Meta': {'object_name': 'SMS'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'delivery_status': ('django.db.models.fields.TextField', [], {'default': "'unknown'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'mobile_number': ('django.db.models.fields.CharField', [], {'max_length': '12'})
        }
    }

    complete_apps = ['sms']