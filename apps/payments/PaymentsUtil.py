from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives, BadHeaderError

from pupil.models import PupilTutorMatch
from tutor.models import Tutor
from django.conf import settings

__author__ = 'freddie'


def get_pupils_for_tutors(request):
    try:
        user = get_user_model().objects.get(email=request.user.email)
        tutor = Tutor.objects.get(user__id=user.id)
        return [(matches.id, matches.get_prog_report_unicode) for matches in
                PupilTutorMatch.objects.filter(tutor__id=tutor.id).filter(lessons_remaining__gt=0)]
    except (get_user_model().DoesNotExist, Tutor.DoesNotExist):
        return PupilTutorMatch.objects.none()


# This is awful - too many side effects. Lesson save should take parameters and trigger saves of other models via signals - or many in the save method
def register_lesson(lesson, amount, form, payment_record, pupil_tutor_match, duration):
    lesson.save()
    payment_record.amount += amount
    payment_record.save()
    # Update lessons taught
    pupil_tutor_match.lessons_taught += duration
    pupil_tutor_match.save()
    # saving form
    prog = form.save(commit=False)
    prog.lesson = lesson
    prog.save()


def send_prog_report_to_pupil(form, pupil, pupil_tutor_match):
    email_subject = 'Progress report for ' + pupil.name

    # I've got to make the kak better
    email_message = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title></title></head><body><p>Dear ' \
                    'parent/guardian<p><p>Please see below progress report for <strong>' + pupil.name + '</strong>.</p><p>' \
                                                                                                        '<strong>Homework completion status: </strong>' + \
                    form.cleaned_data[
                        'homework_status'] + '<p><p><strong>Tutor summary of ' + pupil.name + '\'s progress: </strong>' + \
                    form.cleaned_data[
                        'student_summary'] + '. We encourage you to discuss further with ' + pupil_tutor_match.tutor \
                        .name + '.' + '<p><p><strong>Homework given: </strong>' + \
                    form.cleaned_data[
                        'homework_summary'] + '<p><p><strong>Lessons remaining: </strong>' + \
                    str(pupil_tutor_match.lessons_remaining) + \
                    '<p><strong>Duration of Lesson: </strong><p>' + str(form.cleaned_data['duration']) + ' hour(s).' \
                                                                                                         '<p>Homework should <strong>always</strong> be given as it is the most important part in the ' \
                                                                                                         'process of improvement. It is absolutely necessary that the homework is not only completed, but ' \
                                                                                                         'that it is completed properly. <strong>Please see to it that homework is completed appropriately' \
                                                                                                         '</strong>. The best time to start is either right after the lesson or the very next day. The ' \
                                                                                                         'homework should be spread evenly over the period between lessons.<p><p><em>Work hard, work smart.' \
                                                                                                         '</em> That is the only route to success.<p></body></html>'
    if not settings.DEBUG:
        email_recipient_pupil = str(pupil.email)
        email_recipient_tutor = str(pupil_tutor_match.tutor.email)
    else:
        print 'sending to freddie'
        email_recipient_pupil = 'freddieodonnell@gmail.com'
        email_recipient_tutor = 'info@tiptoptutors.co.za'
    try:
        mesg = EmailMultiAlternatives(email_subject, '', 'info@tiptoptutors.co.za',
                                      [email_recipient_pupil, email_recipient_tutor])
        mesg.attach_alternative(email_message, 'text/html')
        mesg.send()
    except BadHeaderError:
        pass


def send_email_for_short_lesson_register(dict):
    email_subject = 'Lessons register in short Succession!'

    email_message = dict['name'] + ' registered a lessons with' + dict['pupil'] + ' at ' + dict[
        'now'] + '. Last lesson was ' + dict['last_lesson_time'] \
                    + ' and time between lessons was ' + dict['time_between_lessons']

    email_recipient = 'info@tiptoptutors.co.za'
    try:
        mesg = EmailMultiAlternatives(email_subject, '', 'info@tiptoptutors.co.za',
                                      [email_recipient])
        mesg.attach_alternative(email_message, 'text/html')
        mesg.send()
    except BadHeaderError:
        pass


def find_pupil_pin_in_request(request):
    for value in request.POST:
        if 'pupil_pin' in value:
            return value
    return None
