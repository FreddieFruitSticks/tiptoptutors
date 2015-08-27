# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    depends_on=(
        ('option','0002_auto__add_availabletutorsubject'),
        )

    def forwards(self, orm):
        # Deleting field 'Pupil.subject'
        db.delete_column(u'pupil_pupil', 'subject')

        # Adding field 'Pupil.tutor'
        db.add_column(u'pupil_pupil', 'tutor',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tutor.Tutor'], null=True, blank=True),
                      keep_default=False)

        # Adding M2M table for field subject on 'Pupil'
        m2m_table_name = db.shorten_name(u'pupil_pupil_subject')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pupil', models.ForeignKey(orm[u'pupil.pupil'], null=False)),
            ('availabletutorsubject', models.ForeignKey(orm[u'option.availabletutorsubject'], null=False))
        ))
        db.create_unique(m2m_table_name, ['pupil_id', 'availabletutorsubject_id'])


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Pupil.subject'
        raise RuntimeError("Cannot reverse this migration. 'Pupil.subject' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Pupil.subject'
        db.add_column(u'pupil_pupil', 'subject',
                      self.gf('django.db.models.fields.CharField')(max_length=50),
                      keep_default=False)

        # Deleting field 'Pupil.tutor'
        db.delete_column(u'pupil_pupil', 'tutor_id')

        # Removing M2M table for field subject on 'Pupil'
        db.delete_table(db.shorten_name(u'pupil_pupil_subject'))


    models = {
        u'option.availabletutorsubject': {
            'Meta': {'object_name': 'AvailableTutorSubject'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'option.city': {
            'Meta': {'object_name': 'City'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'option.levelofstudy': {
            'Meta': {'object_name': 'LevelOfStudy'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'pupil.pupil': {
            'Meta': {'object_name': 'Pupil'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['option.City']"}),
            'contact_number': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level_of_study': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['option.LevelOfStudy']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'requirement': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'subject': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['option.AvailableTutorSubject']", 'symmetrical': 'False'}),
            'suburb': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'tutor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tutor.Tutor']", 'null': 'True', 'blank': 'True'})
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

    complete_apps = ['pupil']