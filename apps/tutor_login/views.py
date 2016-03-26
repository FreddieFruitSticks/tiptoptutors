from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context_processors import csrf
from django.views.decorators.http import require_http_methods

# from common.forms import UserTutorSignupForm
from forms import UserTutorSignupForm
from payments.models import PaymentRecord
from tutor.models import Tutor
from matchmaker.models import PupilTutorMatch


@require_http_methods("POST")
def register_user(request):
    form = UserTutorSignupForm(request.POST)
    if form.is_valid():
        form.save()
        user = auth.authenticate(email=request.POST.get('username', ''), password=request.POST.get('password1', ''))
        print(request.POST.get('password1', ''))
        print('I am here')
        print(user)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect('/tutor/')
        return HttpResponseRedirect('/tutor-invalid/')
    # elif not request.POST.get('password1', '') == request.POST.get('password2', ''):
    #     return HttpResponseRedirect('/tutor-invalid-pass/')
    else:
        return invalid_registration(request)


# @login_required(login_url="/")
def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    print (password)
    user = auth.authenticate(username=username, password=password)

    print(get_current_site(request))
    if user is not None:
        auth.login(request, user)
        if Tutor.objects.filter(user=user.id).count() > 0:
            return tutor_pupil_summary(request)
        return HttpResponseRedirect('/tutor/')
    else:
        return invalid_login(request)


# @login_required(login_url="/")
def loggedin(request):
    return render_to_response('loggedin.html', {'firstname': request.user.username})


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


def invalid_login(request):
    args = {}
    args.update(csrf(request))
    return render_to_response('invalid-login.html', args)


def invalid_registration(request):
    args = {}
    args.update(csrf(request))
    return render_to_response('form-something-wrong.html', args)


def invalid_pass(request):
    args = {}
    args.update(csrf(request))
    return render_to_response('invalid-tutor-pass.html', args)


@login_required(login_url="/")
def tutor_pupil_summary(request):
    return HttpResponseRedirect('/progressreport/')


@login_required(login_url="/")
def tutor_faq(request):
    args = {}
    args.update(csrf(request))
    return render_to_response('faq.html', args)


@login_required(login_url="/")
def pupil_credits(request):
    args = {}
    args.update(csrf(request))

    pupils = PupilTutorMatch.objects.filter(tutor__id=Tutor.objects.filter(user__id=request.user.id))
    try:
        money = PaymentRecord.objects.filter(tutor__id=Tutor.objects.filter(user__id=request.user.id)).get(paid=False)
    except PaymentRecord.DoesNotExist:
        money = None

    args['money'] = money
    args['pupils'] = pupils
    return render_to_response('pupils-credits.html', args)


# class RecoveryPage(Recover):
#     form_class = PasswordRecoveryForm
#
#     def get(self, request, *args, **kwargs):

