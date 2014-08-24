from django.contrib import admin

from models import Tutor


class TutorAdmin(admin.ModelAdmin):
    search_fields = [ "name", 'surname', 'mobile', 'email', 'subject' ]
    list_display  =  ("name", 'surname', 'mobile', 'email',
                      'related_information', 'documents')
    list_filter   = ('subject',)
    raw_id_fields = ('id_doc', 'cv', 'academic')

    fieldsets = (
        ('Admin', {
            'fields': ('status', 'comment')
        }),

        ('Tutor details', {
            'fields': ('name', 'surname', 'mobile', 'email',
                       'subject', 'transport', 'id_passport',
                       'id_doc', 'cv', 'academic')
        }),
    )

    def related_information(self, obj):
        my_urls = ""

    #    if not obj.comment_set.all().count():
    #        actions += '<a cl

        if not obj.pupil_set.all().count():
            my_urls += '<a class="admin_pupil" href="/admin/pupil/?project__id__exact=%s"><img src="/static/images/icons/comment.png" alt="comments" title="comments"/></a>' % obj.id
        return my_urls
    related_information.allow_tags = True

    def documents(self, obj):
        output = ''
        for doc_name, label in zip(('id_doc', 'cv', 'academic'),
                                   ('ID', 'CV', 'transcript')):
            if getattr(obj, '%s_id' % doc_name, None) is None:
                output += 'No %s</br>' % label
            else:
                url = getattr(obj, doc_name).get_absolute_url()
                output += '<a href="%s">Download %s</a></br>' % (url, label)
        return output
    documents.allow_tags = True


admin.site.register(Tutor, TutorAdmin)

