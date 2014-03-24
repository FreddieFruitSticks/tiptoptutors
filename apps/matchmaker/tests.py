from datetime import datetime

from django.test import TestCase

from apps.tutor.models import Tutor
from apps.option.models import AvailableTutorSubject
from apps.pupil.models import Pupil, PupilTutorMatch
from apps.matchmaker.models import PupilProxy, TutorProxy


class MatchmakerTestCase(TestCase):
    fixtures = ['test_data.json']

    def setUp(self):
        self.tutor = TutorProxy.objects.all()[0]
        self.pupil = PupilProxy.objects.all()[0]

    def tearDown(self):
        PupilTutorMatch.objects.all().delete()

    def create_tutor_for_subjects(self, pupil, subjects):
        tutor = Tutor.objects.create(**{
                'name': 'Name',
                'surname': 'Surname',
                'email': 'name@example.com',
                'mobile': '1234567890',
                'id_passport': '123456789012',
                'id_doc': 'image.jpg',
                'status': 'Accepted',
        })
        tutor.subject.add(*subjects)
        for subject in tutor.subject.all():
            PupilTutorMatch.objects.create(pupil=pupil,
                                           tutor=tutor,
                                           subject=subject,
                                           start_date=datetime.utcnow().date())
        return tutor

    def assign_tutor_for_subjects(self, pupil, tutor, subjects=None):
        if subjects is None:
            subjects = tutor.subject.all().values_list('pk', flat=True)
        for subject_pk in subjects:
            if isinstance(subject_pk, AvailableTutorSubject):
                subject_pk = subject_pk.pk
            PupilTutorMatch.objects.create(pupil=pupil,
                                           tutor=tutor,
                                           subject_id=subject_pk,
                                           start_date=datetime.utcnow().date())

    def test_some_unmatched(self):
        # No subjects matched up
        self.assertTrue(PupilProxy.objects.some_unmatched()
                                          .filter(pk=self.pupil.pk).exists())
        self.assertEqual(list(self.pupil.unmatched_subjects),
                         list(AvailableTutorSubject.objects.all()))
        # Assign tutor for 2 out of 4 subjects
        self.assign_tutor_for_subjects(self.pupil, self.tutor, [2, 4])
        # Check that the pupil is still classified as needing a tutor (for 2 subjects)
        self.assertTrue(PupilProxy.objects.some_unmatched()
                                          .filter(pk=self.pupil.pk).exists())
        self.assertTrue(
            list(self.pupil.unmatched_subjects.values_list('pk', flat=True)),
            [1, 3]
        )
        # Assign tutor for the remaining subjects
        self.create_tutor_for_subjects(self.pupil, [1, 3])
        self.assertEqual(PupilProxy.objects.some_unmatched().count(), 0)

    def test_all_matched(self):
        # No subjects matched up
        #self.assertFalse(PupilProxy.objects.all_matched()
        #                                   .filter(pk=self.pupil.pk).exists())
        # Assign tutor for 2 out of 4 subjects
        self.assign_tutor_for_subjects(self.pupil, self.tutor, [2, 4])
        # Check that the pupil is still classified as needing a tutor (for 2 subjects)
        self.assertFalse(PupilProxy.objects.all_matched()
                                           .filter(pk=self.pupil.pk).exists())
        # Create tutor for the remaining subjects
        self.create_tutor_for_subjects(self.pupil, [1, 3])
        # Check that pupil is classified as not needing a tutor
        self.assertTrue(PupilProxy.objects.all_matched()
                                          .filter(pk=self.pupil.pk).exists())
        # Check that no unmatched subjects remain
        self.assertEqual(self.pupil.unmatched_subjects.count(), 0)
