from django.db import models
from tinymce.models import HTMLField
# from autoslug import AutoSlugField


class HomePageControler(models.Model):
    introduction_desc = HTMLField(default='')
    detection_desc = HTMLField(default='')

    # new_slag = AutoSlugField(populate_from = 'news_title', unique=True, null=True, default=None)


# Create your models here.
