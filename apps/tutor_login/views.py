from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context_processors import csrf
from django.views.decorators.http import require_http_methods
from common.forms import TutorSignupForm
from tutor.views import tutor_login_frontpage


@require_http_methods("POST")
def register_user(request):
    form = TutorSignupForm(request.POST)
    if form.is_valid():
        form.save()
        args = {}
        args.update(csrf(request))
        return tutor_login_frontpage(request)
    else:
        invalid_login(request)


def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request, user)
        # return HttpResponseRedirect('/loggedin/')
        return tutor_pupil_summary(request)
    else:
        return render_to_response('invalid-login.html')


@login_required(login_url="/")
def loggedin(request):
    return render_to_response('loggedin.html', {'firstname': request.user.username})


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


def invalid_login(request):
    return render_to_response('invalid-login.html')


@login_required(login_url="/")
def tutor_pupil_summary(request):
    return HttpResponseRedirect('/loggedin/')


@login_required(login_url="/")
def tutor_faq(request):
    return render_to_response('faq.html')


@login_required(login_url="/")
def register_lesson(request):
    return render_to_response('regiter-lesson.html')


@login_required(login_url="/")
def pupil_credits(request):
    return render_to_response('pupils-credits.html')


@login_required(login_url="/")
def lesson_history(request):
    return render_to_response('lesson-history.html')
