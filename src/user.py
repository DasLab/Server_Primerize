from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, HttpResponseServerError
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, render_to_response

from filemanager import FileManager

from src.models import *


def user_login(request):
    if request.user.is_authenticated():
        if request.GET.has_key('next') and 'admin' in request.GET['next']:
            return error403(request)
        return HttpResponseRedirect('/')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        messages = 'Invalid username and/or password. Please try again.'
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            flag = form.cleaned_data['flag']
            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    if flag == "Admin":
                        return HttpResponseRedirect('/admin/')
                    else:
                        return HttpResponseRedirect('/')
                else:
                    messages = 'Inactive/disabled account. Please contact us.'
        return render_to_response(PATH.HTML_PATH['login'], {'form': form, 'messages': messages}, context_instance=RequestContext(request))
    else:
        if request.GET.has_key('next') and 'admin' in request.GET['next']:
            flag = 'Admin'
        else:
            flag = 'Member'
        form = LoginForm(initial={'flag': flag})
        return render_to_response(PATH.HTML_PATH['login'], {'form': form}, context_instance=RequestContext(request))

@login_required
def user_password(request):
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password_old = form.cleaned_data['password_old']
            password_new = form.cleaned_data['password_new']
            password_new_rep = form.cleaned_data['password_new_rep']
            if password_new != password_new_rep:
                return render_to_response(PATH.HTML_PATH['password'], {'form': form, 'messages': 'New password does not match. Please try again.'}, context_instance=RequestContext(request))
            if password_new == password_old:
                return render_to_response(PATH.HTML_PATH['password'], {'form': form, 'messages': 'New password is the same as current. Please try again.'}, context_instance=RequestContext(request))

            user = authenticate(username=username, password=password_old)
            if user is not None:
                u = User.objects.get(username=username)
                u.set_password(password_new)
                u.save()
                logout(request)
                return render_to_response(PATH.HTML_PATH['password'], {'form': form, 'notices': 'Password change successful. Please sign in using new credentials.'}, context_instance=RequestContext(request))
        form = PasswordForm(initial={'username': request.user.username})
        return render_to_response(PATH.HTML_PATH['password'], {'form': form, 'messages': 'Invalid username and/or current password, or missing new password.<br/>Please try again.'}, context_instance=RequestContext(request))
    else:
        form = PasswordForm(initial={'username': request.user.username})
        return render_to_response(PATH.HTML_PATH['password'], {'form': form}, context_instance=RequestContext(request))

def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/")


@user_passes_test(lambda u: u.is_superuser)
def browse(request, path):
    fm = FileManager(MEDIA_ROOT + '/data')
    return fm.render(request, path)
