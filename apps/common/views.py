from django.contrib import auth
from django.shortcuts import get_object_or_404, render_to_response
from django.template.context_processors import csrf
from django.utils.encoding import smart_str
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect

from forms import TutorSignupForm
from tutor.views import tutor_view_form
from models import Document


class HomeView(TemplateView):
    template_name = "common/index.html"


class AboutView(TemplateView):
    template_name = "common/about.html"


class HowThisWorksView(TemplateView):
    template_name = "common/how-this-works.html"


class SubjectsView(TemplateView):
    template_name = "common/subjects.html"


class LibraryView(TemplateView):
    template_name = "common/library.html"


class TermsAndConditionsView(TemplateView):
    template_name = "common/termsandconditions.html"


def serve_document(request, doc_id):
    doc = get_object_or_404(Document, id=doc_id)
    # return 403 if the doc is not public and the user is not staff
    if not doc.is_public and (not hasattr(request, 'user') or
                                  not request.user.is_authenticated() or
                                  not request.user.is_staff):
        return HttpResponseForbidden()

    response = HttpResponse(doc.data, content_type=doc.mime_type)
    response['Content-Disposition'] = ('attachment; filename="%s"'
                                       % smart_str(doc.name))
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Expires'] = '0'
    response['Pragma'] = 'no-store, no-cache'
    return response
