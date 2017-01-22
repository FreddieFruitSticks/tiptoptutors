import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.utils.decorators import method_decorator
from django.views.generic import CreateView
from django.template.context_processors import csrf

from PaymentsUtil import get_pupils_for_tutors, send_email_for_short_lesson_register, \
    register_lesson, send_prog_report_to_pupil
from forms import ProgressReportForm
from models import LessonRecord, PaymentRecord
from pupil.models import PupilTutorMatch, PupilPin
from tutor.models import Tutor


class ProgressReportView(CreateView):
    form_class = ProgressReportForm
    template_name = 'progress_reports/progress_report.html'

    @method_decorator(login_required(login_url='/'))
    def dispatch(self, *args, **kwargs):
        return super(ProgressReportView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):

        form = self.form_class(student=get_pupils_for_tutors(request))

        dictionary = {}
        dictionary.update(csrf(request))
        dictionary['form'] = form

        return render_to_response(self.template_name, dictionary)

    def post(self, request, *args, **kwargs):
        if request.user is None:
            return render_to_response('progress_reports/user_does_not_exist.html')

        form = self.form_class(request.POST, student=get_pupils_for_tutors(request))

        if form.is_valid():
            try:
                pupil_tutor_match = PupilTutorMatch.objects.get(id=form.cleaned_data['pupil'])
            except PupilTutorMatch.DoesNotExist:
                pupil_tutor_match = None
            if pupil_tutor_match is not None:
                try:
                    pupil_pin = PupilPin.objects.get(pupil__id=pupil_tutor_match.pupil.id)
                except PupilPin.DoesNotExist:
                    return render_to_response('progress_reports/pupil_has_no_pin.html')

                pupil = pupil_tutor_match.pupil
                tutor = pupil_tutor_match.tutor
                subject = pupil_tutor_match.subject
                duration_ = form.cleaned_data['duration']
                amount = pupil.level_of_study.rate_category.rate * duration_
                minTimeBetweenLessons = 0

                try:
                    last_lesson_time = LessonRecord.objects.filter(pupil=pupil_tutor_match.pupil).latest(
                        field_name='datetime').datetime
                    time_between_lessons = (datetime.datetime.now() - last_lesson_time.replace(
                        tzinfo=None)).total_seconds() - 7200
                except LessonRecord.DoesNotExist:
                    # poor cheap hack becasue its 1:30am
                    time_between_lessons = minTimeBetweenLessons + 1

                if time_between_lessons > minTimeBetweenLessons:
                    if form.cleaned_data['pupil_pin'] == pupil_pin.pin:
                        try:
                            payment_record = PaymentRecord.objects.filter(paid=False).filter(tutor=tutor).first()
                        except PaymentRecord.DoesNotExist:
                            payment_record = None

                        if payment_record is not None:
                            if pupil_tutor_match.lessons_remaining >= duration_:
                                lesson = LessonRecord(pupil=pupil, tutor=tutor, subject=subject, amount=amount,
                                                      payment_record=payment_record)
                                register_lesson(lesson, amount, form, payment_record, pupil_tutor_match, duration_)
                                send_prog_report_to_pupil(form, pupil, pupil_tutor_match)

                            else:
                                return render_to_response('progress_reports/out_of_lessons.html',
                                                          {'pupil_name': pupil.name})
                        else:
                            if pupil_tutor_match.lessons_remaining > duration_:
                                lesson = LessonRecord(pupil=pupil, tutor=tutor, subject=subject, amount=amount,
                                                      payment_record=payment_record)
                                payment_record = PaymentRecord(amount=0, tutor=tutor, paid=False)
                                payment_record.save()
                                register_lesson(lesson, amount, form, payment_record, pupil_tutor_match, duration_)
                                send_prog_report_to_pupil(form, pupil, pupil_tutor_match)
                            else:
                                return render_to_response('progress_reports/out_of_lessons.html',
                                                          {'pupil_name': pupil.name})

                        form.save()
                        return render_to_response('progress_reports/registered_lesson_success.html')
                    return render_to_response('progress_reports/incorrect_pin.html')
                else:
                    send_email_for_short_lesson_register(
                        {'name': tutor.name, 'pupil': pupil.name, 'last_lesson_time': str(last_lesson_time),
                         'now': str(datetime.datetime.now())
                            , 'time_between_lessons': str(time_between_lessons)})
                    return render_to_response('progress_reports/simple_message_format.html',
                                              {'message': 'Cannot register lessons in short succession'})
            else:
                return render_to_response('progress_reports/user_dne.html')
        else:
            dictionary = {}
            dictionary.update(csrf(request))
            dictionary['form'] = form

            return render_to_response('progress_reports/progress_report.html', dictionary)

    def get_success_url(self):
        return reverse('registerlessonsuccess')


@login_required(login_url='/')
def prog_report_success(request):
    return render_to_response('progress_reports/registered_lesson_success.html')


class LessonHistory(CreateView):
    @method_decorator(login_required(login_url='/'))
    def dispatch(self, *args, **kwargs):
        return super(LessonHistory, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        # user = get_user_model().objects.get(username=request.user)
        # tutor = Tutor.objects.get(user__id=get_user_model().objects.get(username=request.user).id)
        try:
            lesson_records = LessonRecord.objects.filter(
                tutor=Tutor.objects.get(user__id=get_user_model().objects.get(email=request.user.email).id))
        except (LessonRecord.DoesNotExist, Tutor.DoesNotExist, get_user_model().DoesNotExist):
            lesson_records = None

        args = {}
        args.update(csrf(request))
        args['lesson_records'] = lesson_records.order_by('-datetime')
        return render_to_response('progress_reports/lesson_history.html', args)
