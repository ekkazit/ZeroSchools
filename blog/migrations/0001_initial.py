# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import blog.models
import tinymce.models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0002_auto_20150616_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=150)),
                ('short', models.CharField(max_length=50, null=True, blank=True)),
                ('email', models.EmailField(max_length=100, null=True, blank=True)),
                ('phone', models.CharField(max_length=30, null=True, blank=True)),
                ('image', models.FileField(null=True, upload_to=blog.models.get_file_path, blank=True)),
                ('description', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('slug', models.CharField(max_length=200, null=True, blank=True)),
                ('preview', models.TextField(null=True, blank=True)),
                ('description', tinymce.models.HTMLField(null=True, blank=True)),
                ('views', models.IntegerField(default=0)),
                ('is_publish', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('image', models.FileField(null=True, upload_to=blog.models.get_file_path, blank=True)),
                ('author', models.ForeignKey(blank=True, to='blog.Author', null=True)),
                ('category', models.ForeignKey(blank=True, to='blog.Category', null=True)),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
        ),
    ]
