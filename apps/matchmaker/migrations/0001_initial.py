# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'RequestForTutor'
        db.create_table(u'matchmaker_requestfortutor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pupil', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pupil.Pupil'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='active', max_length=8)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=12)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'matchmaker', ['RequestForTutor'])

        # Adding M2M table for field subjects on 'RequestForTutor'
        m2m_table_name = db.shorten_name(u'matchmaker_requestfortutor_subjects')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('requestfortutor', models.ForeignKey(orm[u'matchmaker.requestfortutor'], null=False)),
            ('availabletutorsubject', models.ForeignKey(orm[u'option.availabletutorsubject'], null=False))
        ))
        db.create_unique(m2m_table_name, ['requestfortutor_id', 'availabletutorsubject_id'])

        # Adding model 'RequestSMS'
        db.create_table(u'matchmaker_requestsms', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('request', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['matchmaker.RequestForTutor'])),
            ('tutor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tutor.Tutor'])),
            ('delivery_status', self.gf('django.db.models.fields.CharField')(default='unknown', max_length=16)),
            ('response_text', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('response_timestamp', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'matchmaker', ['RequestSMS'])


    def backwards(self, orm):
        # Deleting model 'RequestForTutor'
        db.delete_table(u'matchmaker_requestfortutor')

        # Removing M2M table for field subjects on 'RequestForTutor'
        db.delete_table(db.shorten_name(u'matchmaker_requestfortutor_subjects'))

        # Deleting model 'RequestSMS'
        db.delete_table(u'matchmaker_requestsms')


    models = {
        u'matchmaker.requestfortutor': {
            'Meta': {'object_name': 'RequestForTutor'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '12'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pupil': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['pupil.Pupil']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'active'", 'max_length': '8'}),
            'subjects': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['option.AvailableTutorSubject']", 'symmetrical': 'False'})
        },
        u'matchmaker.requestsms': {
            'Meta': {'object_name': 'RequestSMS'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'delivery_status': ('django.db.models.fields.CharField', [], {'default': "'unknown'", 'max_length': '16'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'request': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['matchmaker.RequestForTutor']"}),
            'response_text': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'response_timestamp': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'tutor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['tutor.Tutor']"})
        },
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

    complete_apps = ['matchmaker']