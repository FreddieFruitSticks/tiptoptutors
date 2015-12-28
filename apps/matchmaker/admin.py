from django.core.urlresolvers import reverse
from django.conf.urls import patterns, url
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext, Template, Context, TemplateSyntaxError, Engine, TemplateDoesNotExist

from pupil.admin import PupilTutorMatchAdmin
from option.models import AvailableTutorSubject
from matchmaker import models
from matchmaker.tasks import send_tutor_request_smses


class FilterByTutorStatus(SimpleListFilter):
    title = 'tutor status'
    parameter_name = 'has_tutor'

    def lookups(self, request, model_admin):
        return (('1', 'Has tutor(s) for all subjects'),
                ('0', 'Needs a tutor for one or more subjects'))

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.all_matched()
        elif self.value() == '0':
            return queryset.some_unmatched()


class FilterByPaidStatus(SimpleListFilter):
    title = 'Paid or not Paid'
    parameter_name = 'has_paid'

    def lookups(self, request, model_admin):
        return (('0', 'Paid'),
                ('1', 'Not Paid'))

    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.paid()
        elif self.value() == '1':
            return queryset.unpaid()


class FilterByActiveStatus(SimpleListFilter):
    title = 'Lessons remaining (has paid)'
    parameter_name = 'lessons_remaining'

    def lookups(self, request, model_admin):
        return (('0', 'Has lessons remaining'),
                ('1', 'No lessons remaining'),
                ('2', 'Two lessons remaining'))

    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.actively_tutored()
        elif self.value() == '1':
            return queryset.finished_lessons()
        elif self.value() == '2':
            return queryset.two_lessons_remaining()


def label_from_tutor_instance(pupil_subject_pks):
    def inner(obj):
        return '%s (%s)' % (
            obj.__unicode__(),
            ', '.join(s.name for s in obj.matching_subjects(pupil_subject_pks))
        )

    return inner


class SMSTutorsForm(forms.Form):
    _template_engine = Engine.get_default()
    pupil = forms.ModelChoiceField(
        queryset=models.PupilProxy.objects.all(),
        widget=forms.HiddenInput,
        label='',
    )
    matching_tutors = forms.ModelMultipleChoiceField(
        queryset=models.TutorProxy.objects.all(),
    )
    sms_text = forms.CharField(
        max_length=200,
        widget=forms.Textarea,
        label='SMS text'
    )

    @classmethod
    def load_sms_template_source(cls):
        for loader in cls._template_engine.template_loaders:
            try:
                return loader.load_template_source('matchmaker/sms_request_for_tutor.txt'
                                                   )[0]
            except TemplateDoesNotExist:
                pass
        raise TemplateDoesNotExist('matchmaker/sms_request_for_tutor.txt')

    def __init__(self, *args, **kwargs):
        if 'pupil' not in kwargs:
            raise TypeError("argument 'pupil' is required")
        new_kwargs = kwargs.copy()
        pupil = new_kwargs.pop('pupil')
        initial = {
            'pupil': pupil,
            'sms_text': self.load_sms_template_source()
        }
        initial.update(new_kwargs.pop('initial', {}))
        super(SMSTutorsForm, self).__init__(*args, initial=initial, **new_kwargs)

        self.pupil_obj = pupil
        # NB: only show unmatched subjects
        self.pupil_subject_pks = list(pupil.unmatched_subjects.values_list('pk', flat=True))
        self.fields['matching_tutors'].queryset = models.TutorProxy.objects \
            .filter(subject__in=self.pupil_subject_pks) \
            .filter(status__iexact='Accepted') \
            .distinct()
        self.fields['matching_tutors'].label_from_instance = \
            label_from_tutor_instance(self.pupil_subject_pks)
        try:
            rendered_sms = self.render_sms_text()
            self.fields['sms_text'].help_text = (
                "%s</br></br><strong>(%d out of 140 characters)</strong>"
                % (rendered_sms.replace('\n', '<br/>'), len(rendered_sms))
            )
        except TemplateSyntaxError:
            pass

    def render_sms_text(self, context=None):
        if self.is_bound:
            template = Template(self.data['sms_text'])
        else:
            template = Template(self.initial['sms_text'])
        if context is None:
            context = Context({
                'level': 'Grade 11',
                'objects': [{'subject': 'English', 'code': '123456'},
                            {'subject': 'Chemistry', 'code': '456789'}]
            })
        return template.render(context)

    def clean_sms_text(self):
        try:
            self.render_sms_text()
        except TemplateSyntaxError as e:
            raise forms.ValidationError("%s" % e)
        return self.data['sms_text']

    def clean(self):
        c_data = super(SMSTutorsForm, self).clean()
        return c_data

    def save(self, request):
        # get intersection of subjects required and tutors selected
        subjects = AvailableTutorSubject.objects.filter(
            tutor__in=self.cleaned_data['matching_tutors'],
            pk__in=self.pupil_subject_pks)
        # check if there is already an active request for required subjects
        # if there is, use that to send SMS
        # if there isn't, create a request
        subject_requests = {}
        for subject in subjects:
            rft = models.RequestForTutor.objects.filter(
                pupil=self.cleaned_data['pupil'],
                subject=subject,
                status='active'
            ).order_by('-created')
            if rft:
                rft = rft[0]
            else:
                rft = models.RequestForTutor.objects.create(
                    pupil=self.cleaned_data['pupil'],
                    subject=subject
                )
            subject_requests[subject.pk] = rft
        # match subjects to tutors
        tutor_pks = []
        request_pks = []
        for tutor in self.cleaned_data['matching_tutors']:
            tutor_pks.append(tutor.pk)
            request_pks.append([subject_requests[s.pk].pk for s in
                                tutor.subject.filter(pk__in=subjects)
                                if s.pk in subject_requests])
        # send smses (TODO: use celery)
        send_tutor_request_smses(tutor_pks, request_pks,
                                 self.cleaned_data['sms_text'])


class PupilMatchingAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'needs_tutor', 'per_pupil_actions']
    list_filter = [FilterByTutorStatus, FilterByPaidStatus, FilterByActiveStatus]
    actions = None
    inlines = [PupilTutorMatchAdmin]

    def select_tutors(self, request, pk):
        pupil = models.PupilProxy.objects.get(pk=pk)
        if request.method == 'POST':
            form = SMSTutorsForm(request.POST, pupil=pupil)
            if form.is_valid():
                form.save(request)
                return HttpResponseRedirect(reverse('admin:matchmaker_pupilproxy_changelist'))
        else:
            form = SMSTutorsForm(pupil=pupil)
        return render_to_response('admin/matchmaker/select-tutors.html',
                                  {'form': form},
                                  context_instance=RequestContext(request))

    def get_urls(self):
        urls = super(PupilMatchingAdmin, self).get_urls()
        return patterns('',
                        url(
                            '^(?P<pk>\d+)/select-tutors/$',
                            self.admin_site.admin_view(self.select_tutors),
                            name='select-tutors'
                        ),
                        ) + urls

    def per_pupil_actions(self, obj):
        return '<a href="%s">SMS tutors</a>' % \
               reverse('admin:select-tutors', kwargs={'pk': obj.pk})

    per_pupil_actions.allow_tags = True
    per_pupil_actions.short_description = 'Actions'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class RequestSMSAdmin(admin.ModelAdmin):
    list_display = ['id', 'pupil', 'tutor', 'subjects', 'matched_subjects',
                    'response_text', 'response_timestamp']

    def pupil(self, obj):
        requests = obj.requests.all()
        if requests:
            return requests[0].pupil.full_name
        return None

    def subjects(self, obj):
        return ', '.join([str(o.subject) for o in obj.requests.all()])

    def matched_subjects(self, obj):
        matched = obj.requests.filter(code__in=obj.codes)
        return ', '.join([str(m.subject) for m in matched])


class RequestForTutorAdmin(admin.ModelAdmin):
    list_display = ['id', 'pupil_full_name', 'subject', 'status', 'code', 'created']

    def pupil_full_name(self, obj):
        return obj.pupil.full_name

    pupil_full_name.short_description = 'pupil'


admin.site.register(models.PupilProxy, PupilMatchingAdmin)
admin.site.register(models.RequestForTutor, RequestForTutorAdmin)
admin.site.register(models.RequestSMS, RequestSMSAdmin)
admin.site.register(models.PupilSubjectMatch)
