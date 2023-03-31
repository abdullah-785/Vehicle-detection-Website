# Generated by Django 4.1.7 on 2023-03-28 05:32

import autoslug.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HomePageControler',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('introduction_desc', autoslug.fields.AutoSlugField(default=None, editable=False, null=True, populate_from='news_title', unique=True)),
                ('detection_desc', autoslug.fields.AutoSlugField(default=None, editable=False, null=True, populate_from='news_title', unique=True)),
            ],
        ),
    ]