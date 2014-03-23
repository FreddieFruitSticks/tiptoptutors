# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PupilTutorMatch'
        db.create_table(u'pupil_pupiltutormatch', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pupil', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pupil.Pupil'])),
            ('tutor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tutor.Tutor'])),
            ('start_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('end_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'pupil', ['PupilTutorMatch'])

        # Adding M2M table for field subject on 'PupilTutorMatch'
        m2m_table_name = db.shorten_name(u'pupil_pupiltutormatch_subject')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('pupiltutormatch', models.ForeignKey(orm[u'pupil.pupiltutormatch'], null=False)),
            ('availabletutorsubject', models.ForeignKey(orm[u'option.availabletutorsubject'], null=False))
        ))
        db.create_unique(m2m_table_name, ['pupiltutormatch_id', 'availabletutorsubject_id'])

        # Deleting field 'Pupil.tutor'
        db.delete_column(u'pupil_pupil', 'tutor_id')


    def backwards(self, orm):
        # Deleting model 'PupilTutorMatch'
        db.delete_table(u'pupil_pupiltutormatch')

        # Removing M2M table for field subject on 'PupilTutorMatch'
        db.delete_table(db.shorten_name(u'pupil_pupiltutormatch_subject'))

        # Adding field 'Pupil.tutor'
        db.add_column(u'pupil_pupil', 'tutor',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tutor.Tutor'], null=True, blank=True),
                      keep_default=False)


    models = {
        u'option.availabletutorsubject': {
            'Meta': {'ordering': "('name',)", 'object_name': 'AvailableTutorSubject'},
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
            'tutor': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['tutor.Tutor']", 'null': 'True', 'through': u"orm['pupil.PupilTutorMatch']", 'blank': 'True'})
        },
        u'pupil.pupiltutormatch': {
            'Meta': {'object_name': 'PupilTutorMatch'},
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pupil': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pupil.Pupil']"}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['option.AvailableTutorSubject']", 'symmetrical': 'False'}),
            'tutor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tutor.Tutor']"})
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