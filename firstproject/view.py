from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .form import userForm
from django.core.paginator import Paginator
from django.core.mail import send_mail


def homePage(request):
    return render(request, "index.html")


def login(request):
    return render(request, 'login.html')


def detection(request):
    return render(request, 'detection.html')

def contactUs(request):
    return render(request, 'contactus.html')

def aboutUs(request):
    return render(request, 'aboutus.html')