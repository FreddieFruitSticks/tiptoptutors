from django.core.urlresolvers import reverse
from django.conf.urls import patterns, url
from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django import forms
from django.shortcuts import render_to_response
from django.template import RequestContext

from matchmaker import models


class FilterByTutorStatus(SimpleListFilter):
    title = 'tutor status'
    parameter_name = 'has_tutor'

    def lookups(self, request, model_admin):
        return (('1', 'Has a tutor'),
                ('0', 'Does not have a tutor'))

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(tutor_id__isnull=False)
        else:
            return queryset.filter(tutor_id__isnull=True)


def label_from_tutor_instance(pupil_subject_pks):
    def inner(obj):
        return '%s (%s)' % (
            obj.__unicode__(),
            ', '.join(s.name for s in obj.matching_subjects(pupil_subject_pks))
        )
    return inner


class SMSTutorsForm(forms.Form):
    pupil = forms.ModelChoiceField(
        queryset=models.PupilProxy.objects.all(),
        widget=forms.HiddenInput,
        label='',
    )
    matching_tutors = forms.ModelMultipleChoiceField(
        queryset=models.TutorProxy.objects.all(),
    )

    def __init__(self, *args, **kwargs):
        if 'pupil' not in kwargs:
            raise TypeError("argument 'pupil' is required")
        new_kwargs = kwargs.copy()
        pupil = new_kwargs.pop('pupil')
        initial = new_kwargs.pop('initial', {'pupil': pupil})
        super(SMSTutorsForm, self).__init__(*args, initial=initial, **new_kwargs)

        self.pupil_obj = pupil
        self.pupil_subject_pks = list(pupil.subject.values_list('pk', flat=True))
        self.fields['matching_tutors'].queryset = models.TutorProxy.objects \
                .filter(subject__in=self.pupil_subject_pks) \
                .filter(status__iexact='Accepted') \
                .distinct()
        self.fields['matching_tutors'].label_from_instance = \
                label_from_tutor_instance(self.pupil_subject_pks)

    def save(self, request):
        raise NotImplementedError('Should prob implement this')


class PupilMatchingAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'has_tutor', 'per_pupil_actions']
    list_filter = [FilterByTutorStatus]
    actions = None

    def select_tutors(self, request, pk):
        pupil = models.PupilProxy.objects.get(pk=pk)
        if request.method == 'POST':
            form = SMSTutorsForm(request.POST, pupil=pupil)
            if form.is_valid():
                form.save(request)
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

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(models.PupilProxy, PupilMatchingAdmin)
