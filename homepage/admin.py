
from django.contrib import admin
from homepage.models import HomePageControler

class HomePageControllerAdmin(admin.ModelAdmin):
    display = ('introduction_desc', 'detection_desc')

admin.site.register(HomePageControler, HomePageControllerAdmin)

# Register your models here.

