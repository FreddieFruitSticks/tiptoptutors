import StringIO
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import loader
from django.template.context import Context
from django.template.loader import get_template
from django import http
from django.utils.encoding import smart_unicode
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
import ho.pisa as pisa
import settings