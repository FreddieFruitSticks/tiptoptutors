from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.utils.decorators import method_decorator
from django.views.generic import CreateView
from django.template.context_processors import csrf

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
            pupil_tutor_match = PupilTutorMatch.objects.get(id=form.cleaned_data['pupil'])
            if pupil_tutor_match is not None:
                pupil_pin = PupilPin.objects.get(pupil__id=pupil_tutor_match.pupil.id)
                pupil = pupil_tutor_match.pupil
                tutor = pupil_tutor_match.tutor
                subject = pupil_tutor_match.subject

                amount = pupil.level_of_study.rate_category.rate
                print(amount)

                if form.cleaned_data['pupil_pin'] == pupil_pin.pin:
                    try:
                        payment_record = PaymentRecord.objects.filter(paid=False).get(tutor=tutor)
                    except PaymentRecord.DoesNotExist:
                        payment_record = None

                    if payment_record is not None:
                        if pupil_tutor_match.lessons_remaining > 0:
                            lesson = LessonRecord(pupil=pupil, tutor=tutor, subject=subject, amount=amount,
                                                  payment_record=payment_record)
                            lesson.save()
                            payment_record.amount += amount
                            payment_record.save()

                            # Update lessons taught
                            pupil_tutor_match.lessons_taught += 1
                            pupil_tutor_match.save()

                            # saving form
                            prog = form.save(commit=False)
                            prog.lesson = lesson
                            prog.save()
                        else:
                            return render_to_response('progress_reports/out_of_lessons.html',
                                                      {'pupil': pupil.name})
                    else:
                        if pupil_tutor_match.lessons_remaining > 0:
                            payment_record = PaymentRecord(amount=0, tutor=tutor, paid=False)
                            payment_record.save()
                            lesson = LessonRecord(pupil=pupil, tutor=tutor, subject=subject, amount=amount,
                                                  payment_record=payment_record)
                            lesson.save()
                            payment_record.amount += amount
                            payment_record.save()

                            # Update lessons taught
                            pupil_tutor_match.lessons_taught += 1
                            pupil_tutor_match.save()

                            # saving form
                            prog = form.save(commit=False)
                            prog.lesson = lesson
                            prog.save()
                        else:
                            return render_to_response('progress_reports/out_of_lessons.html',
                                                      {'pupil': pupil.name})

                    return render_to_response('progress_reports/registered_lesson_success.html')
                return render_to_response('progress_reports/incorrect_pin.html')
            else:
                return render_to_response('progress_reports/user_dne.html')
        else:
            dictionary = {}
            dictionary.update(csrf(request))
            dictionary['form'] = form

            return render_to_response('progress_reports/progress_report.html', dictionary)

    def get_success_url(self):
        return reverse('registerlessonsuccess')


def prog_report_success(request):
    return render_to_response('progress_reports/registered_lesson_success.html')


def get_pupils_for_tutors(request):
    try:
        user = User.objects.get(username=request.user)
        tutor = Tutor.objects.get(user__id=user.id)
        return [(matches.id, matches.get_prog_report_unicode) for matches in
                PupilTutorMatch.objects.filter(tutor__id=tutor.id).filter(lessons_remaining__gt=0)]
    except (User.DoesNotExist, Tutor.DoesNotExist):
        return PupilTutorMatch.objects.none()


class LessonHistory(CreateView):

    @method_decorator(login_required(login_url='/'))
    def dispatch(self, *args, **kwargs):
        return super(LessonHistory, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render_to_response('progress_reports/lesson_history.html')
