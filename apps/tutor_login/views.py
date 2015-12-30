from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context_processors import csrf
from django.views.decorators.http import require_http_methods
from common.forms import TutorSignupForm
from tutor.views import tutor_view_form


@require_http_methods("POST")
def register_user(request):
    form = TutorSignupForm(request.POST)
    if form.is_valid():
        form.save()
        args = {}
        args.update(csrf(request))
        return tutor_view_form(request)


def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    print "HEEERE"
    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/loggedin/')
    else:
        return HttpResponseRedirect('/access/invalid')


@login_required(login_url="/")
def loggedin(request):
    return render_to_response('tutor/loggedin.html', {'firstname': request.user.username})


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


def invalid_login(request):
    return HttpResponseRedirect('/')
