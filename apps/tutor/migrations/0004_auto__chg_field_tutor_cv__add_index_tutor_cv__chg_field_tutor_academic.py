# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    depends_on = (
        ("common", "0001_initial"),
    )

    def forwards(self, orm):
        # Deleting field 'Tutor.academic'
        db.delete_column(u'tutor_tutor', 'academic')

        # Deleting field 'Tutor.cv'
        db.delete_column(u'tutor_tutor', 'cv')

        # Deleting field 'Tutor.id_doc'
        db.delete_column(u'tutor_tutor', 'id_doc')

        # Adding field 'Tutor.id_doc'
        db.add_column(u'tutor_tutor', 'id_doc',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='id_tutors', null=True, to=orm['common.Document']),
                      keep_default=False)

        # Adding field 'Tutor.cv'
        db.add_column(u'tutor_tutor', 'cv',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='cv_tutors', null=True, to=orm['common.Document']),
                      keep_default=False)

        # Adding field 'Tutor.academic'
        db.add_column(u'tutor_tutor', 'academic',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='academic_tutors', null=True, to=orm['common.Document']),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Tutor.academic'
        db.add_column(u'tutor_tutor', 'academic',
                      self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Tutor.cv'
        db.add_column(u'tutor_tutor', 'cv',
                      self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Tutor.id_doc'
        raise RuntimeError("Cannot reverse this migration. 'Tutor.id_doc' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Tutor.id_doc'
        db.add_column(u'tutor_tutor', 'id_doc',
                      self.gf('django.db.models.fields.files.FileField')(max_length=100),
                      keep_default=False)

        # Deleting field 'Tutor.id_doc'
        db.delete_column(u'tutor_tutor', 'id_doc_id')

        # Deleting field 'Tutor.cv'
        db.delete_column(u'tutor_tutor', 'cv_id')

        # Deleting field 'Tutor.academic'
        db.delete_column(u'tutor_tutor', 'academic_id')


    models = {
        u'common.document': {
            'Meta': {'object_name': 'Document'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'data': ('django.db.models.fields.BinaryField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        },
        u'option.availabletutorsubject': {
            'Meta': {'ordering': "('name',)", 'object_name': 'AvailableTutorSubject'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'tutor.tutor': {
            'Meta': {'object_name': 'Tutor'},
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_passport': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'2'", 'max_length': '10'}),
            'subject': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['option.AvailableTutorSubject']", 'symmetrical': 'False'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'transport': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['tutor']