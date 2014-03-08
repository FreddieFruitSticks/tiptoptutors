from django.contrib import admin
from models import Tutor


def related_information(obj):

    my_urls = ""

#    if not obj.comment_set.all().count():
#        actions += '<a cl

    if not obj.pupil_set.all().count():
        my_urls += '<a class="admin_pupil" href="/admin/pupil/?project__id__exact=%s"><img src="/static/images/icons/comment.png" alt="comments" title="comments"/></a>' % obj.id
    return my_urls

related_information.allow_tags = True

class TutorAdmin(admin.ModelAdmin):
    search_fields = [ "name", 'surname', 'mobile', 'email', 'subject' ]
    list_display  =  ("name", 'surname', 'mobile', 'email', related_information)
    list_filter   = ('subject',)

    fieldsets = (
        ('Admin', {
            'fields': ('status', 'comment')
        }),

        ('Tutor details', {
            'fields': ('name', 'surname', 'mobile', 'email', 'subject', 'transport', 'id_doc', 'cv', 'academic')
        }),
    )

admin.site.register(Tutor, TutorAdmin)

