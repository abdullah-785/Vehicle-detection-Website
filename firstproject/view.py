from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .form import userForm
from django.core.paginator import Paginator
from homepage.models import HomePageControler
from django.core.mail import send_mail
from django.contrib import auth
# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import firestore
from google.cloud import firestore

import pyrebase


firebaseConfig = {
    'apiKey': "AIzaSyBBU5WLvfTLczxeCtlCxuGrpIK0UKK5Pig",
    'authDomain': "automatedvehicledetection.firebaseapp.com",
    'databaseURL': "https://automatedvehicledetection-default-rtdb.firebaseio.com",
    'projectId': "automatedvehicledetection",
    'storageBucket': "automatedvehicledetection.appspot.com",
    'messagingSenderId': "446921544901",
    'appId': "1:446921544901:web:90eb3bfe0274096f2e8cac",
    'measurementId': "G-HFXP97QT4B"
}
  
firebase = pyrebase.initialize_app(firebaseConfig)
authe = firebase.auth()

db = firebase.database()

# cred = credentials.Certificate('automatedvehicledetection-firebase-adminsdk-e5qn7-82b1849f2a.json')
# firebase_admin.initialize_app(cred)
# db = firestore.Client()

def homePage(request):
    # for display the data from models
    homePageController = HomePageControler.objects.all()
    data = {
        'homePageControler': homePageController,
    }
    return render(request, "index.html", data)


def login(request):
    # checkLogin = True
    return render(request, 'login.html',)


def checkLogin(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    print(email)
    try:
        user = authe.sign_in_with_email_and_password(email,password)    
        uid = user['localId']
        db.child("currentUser").set(uid)
    except:
        message = "Invalid Credential"
        return render(request, "login.html", {'messg': message})
    
    return render(request, 'index.html',)

def detection(request):
    return render(request, 'detection.html')

def contactUs(request):
    return render(request, 'contactus.html')

def aboutUs(request):
    return render(request, 'aboutus.html')

def signup(request):
    return render(request, 'signup.html')

def postsignup(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    confirmPassword = request.POST.get('confirmPassword')
    user = authe.create_user_with_email_and_password(email,password)
    print(email)
    print(password)

    # uid = user['localId']
    data = {'email': email, 'password': password}

    # db.child("notification").child(user['localId']).set(data)
    
    return render(request, 'login.html')

def log(request):
    auth.logout(request)
    return render(request, 'login.html')