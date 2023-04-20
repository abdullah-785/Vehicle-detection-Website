"""firstproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from firstproject import view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home', view.homePage),
    path('login', view.login),
    path('checklogin', view.checkLogin),
    path('detection', include('webcam.urls')),
    path('aboutus', view.aboutUs), 
    path('contactus', view.contactUs),
    path('', view.signup),
    path('postsignup', view.postsignup),
    path('logout', view.log),


    
]
