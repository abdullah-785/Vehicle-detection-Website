from django.contrib import admin
from django.urls import path


from webcam import views
urlpatterns = [
    path('', views.detectionFunc, name='detection'),
    path('video_feed/', views.video_feed, name='video_feed'),
    
]