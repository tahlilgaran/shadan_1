# Create your views here.
import pdb
import json
import time
import random
import datetime

from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponseRedirect
from .forms import SignUpForm


def login_site(request):
    wrong_user_pass = False

    if request.POST.get("signup","") != "":
        return HttpResponseRedirect('/signup/')
    if request.POST.get("forget","") != "":
        return HttpResponseRedirect('/forgetpassword/')

    if request.method == 'POST':

        # if form.is_valid():
            username = request.POST.get("username", "")
            password = request.POST.get("pwd", "")

            user = authenticate(username=username,password=password)

            if user:
                login(request, user)
                url = '/timeline/'+ user.username +'/'
                return HttpResponseRedirect(url)
            else:
                wrong_user_pass = True


    return render(request, "login.html", {
            'wrong_user_pass': wrong_user_pass
        })


def forget_pwd (request):
    sended = 1
    if request.POST.get("signup","") != "":
        return HttpResponseRedirect('/signup/')
    if request.POST.get("cancel","") != "":
        return HttpResponseRedirect('/login/')

    if request.method == 'POST':
        u = User.objects.filter(email=request.POST.get("email", ""))
    
        if not u:
            sended=0
        else:
            sended = 2
            u[0].set_password('123456')
            u[0].save()
    return render(request, "forget.html", {
            'has_send': sended,
        })


def signup(request):
    if request.POST.get("save","") != "":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username,password=password)
            if user:
                login(request, user)
                url = '/timeline/'+ username +'/'
                return HttpResponseRedirect(url)
    elif request.POST.get("cancel","")!= "":
        return HttpResponseRedirect('/login/')
    else:
        form = SignUpForm()

    return render(request,"signup.html",{
        'form': form,
    })

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/login/')