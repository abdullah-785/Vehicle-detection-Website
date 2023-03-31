from django.db import models
from tinymce.models import HTMLField
# from autoslug import AutoSlugField


class HomePageControler(models.Model):
    introduction_desc = models.CharField(max_length=250)
    detection_desc = models.CharField(max_length=250)



# Create your models here.
