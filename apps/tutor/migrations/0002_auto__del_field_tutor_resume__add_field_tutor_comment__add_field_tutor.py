# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Renaming field 'Tutor.resume'
        db.rename_column(u'tutor_tutor', 'resume', 'cv')

        # Adding field 'Tutor.comment'
        db.add_column(u'tutor_tutor', 'comment',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Tutor.surname'
        db.add_column(u'tutor_tutor', 'surname',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20),
                      keep_default=False)

        # Adding field 'Tutor.mobile'
        db.add_column(u'tutor_tutor', 'mobile',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=10),
                      keep_default=False)

        # Adding field 'Tutor.id_passport'
        db.add_column(u'tutor_tutor', 'id_passport',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20),
                      keep_default=False)

        # Adding field 'Tutor.transport'
        db.add_column(u'tutor_tutor', 'transport',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Tutor.id_doc'
        db.add_column(u'tutor_tutor', 'id_doc',
                      self.gf('django.db.models.fields.files.FileField')(default='', max_length=100),
                      keep_default=False)

        # Adding field 'Tutor.academic'
        db.add_column(u'tutor_tutor', 'academic',
                      self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Tutor.status'
        db.add_column(u'tutor_tutor', 'status',
                      self.gf('django.db.models.fields.CharField')(default='2', max_length=10),
                      keep_default=False)

        # Adding M2M table for field subject on 'Tutor'
        m2m_table_name = db.shorten_name(u'tutor_tutor_subject')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tutor', models.ForeignKey(orm[u'tutor.tutor'], null=False)),
            ('availabletutorsubject', models.ForeignKey(orm[u'option.availabletutorsubject'], null=False))
        ))
        db.create_unique(m2m_table_name, ['tutor_id', 'availabletutorsubject_id'])


        # Changing field 'Tutor.created_at'
        db.alter_column(u'tutor_tutor', 'created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

        # Changing field 'Tutor.name'
        db.alter_column(u'tutor_tutor', 'name', self.gf('django.db.models.fields.CharField')(max_length=20))

        # Changing field 'Tutor.email'
        db.alter_column(u'tutor_tutor', 'email', self.gf('django.db.models.fields.EmailField')(max_length=25))

    def backwards(self, orm):

        db.rename_column(u'tutor_tutor', 'cv', 'resume')

        # Deleting field 'Tutor.comment'
        db.delete_column(u'tutor_tutor', 'comment')

        # Deleting field 'Tutor.surname'
        db.delete_column(u'tutor_tutor', 'surname')

        # Deleting field 'Tutor.mobile'
        db.delete_column(u'tutor_tutor', 'mobile')

        # Deleting field 'Tutor.id_passport'
        db.delete_column(u'tutor_tutor', 'id_passport')

        # Deleting field 'Tutor.transport'
        db.delete_column(u'tutor_tutor', 'transport')

        # Deleting field 'Tutor.id_doc'
        db.delete_column(u'tutor_tutor', 'id_doc')

        # Deleting field 'Tutor.academic'
        db.delete_column(u'tutor_tutor', 'academic')

        # Deleting field 'Tutor.status'
        db.delete_column(u'tutor_tutor', 'status')

        # Removing M2M table for field subject on 'Tutor'
        db.delete_table(db.shorten_name(u'tutor_tutor_subject'))


        # Changing field 'Tutor.created_at'
        db.alter_column(u'tutor_tutor', 'created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

        # Changing field 'Tutor.name'
        db.alter_column(u'tutor_tutor', 'name', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Changing field 'Tutor.email'
        db.alter_column(u'tutor_tutor', 'email', self.gf('django.db.models.fields.EmailField')(max_length=255))

    models = {
        u'option.availabletutorsubject': {
            'Meta': {'object_name': 'AvailableTutorSubject'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'tutor.tutor': {
            'Meta': {'object_name': 'Tutor'},
            'academic': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'cv': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '25'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_doc': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
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