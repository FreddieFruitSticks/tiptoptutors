from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'tiptoptutors.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^admin/', include(admin.site.urls)),
                       url(r'', include('common.urls')),
                       url(r'', include('contact.urls')),
                       url(r'', include('pupil.urls')),
                       url(r'', include('tutor.urls')),
                       url(r'^sms/', include('sms.urls')),
                       url(r'', include('quote.urls')),
                       url(r'', include('tutor_login.urls')),
                       url(r'', include('payments.urls')),
                       url(r'', include('password_reset.urls')),
                       )

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += patterns('',
                            url(r'^__debug__/', include(debug_toolbar.urls)),
                            )
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
