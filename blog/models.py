import re
import os
import uuid
from django.db import models
from tinymce.models import HTMLField
from taggit.managers import TaggableManager


def slugify(s):
	""" generate text to slugify url """
	return re.sub('[!@#$%^&*()\\\\/:.""]+', '', s).replace(' ', '-').replace('--', '-').lower()


def get_file_path(instance, filename):
	""" get upload image path """
	ext = filename.split('.')[-1]
	filename = '%s.%s' % (uuid.uuid4(), ext)
	return os.path.join('upload', filename)


class Author(models.Model):
	name = models.CharField(max_length=150)
	short = models.CharField(max_length=50, null=True, blank=True)
	email = models.EmailField(max_length=100, null=True, blank=True)
	phone = models.CharField(max_length=30, null=True, blank=True)
	position = models.CharField(max_length=250, null=True, blank=True)
	image = models.FileField(upload_to=get_file_path, null=True, blank=True)
	description = models.TextField(null=True, blank=True)

	def __unicode__(self):
		return self.name


class Category(models.Model):
	name = models.CharField(max_length=200)
	description = models.TextField(null=True, blank=True)

	def __unicode__(self):
		return self.name


class Post(models.Model):
	title = models.CharField(max_length=200)
	slug = models.CharField(max_length=200, null=True, blank=True)
	preview = models.TextField(null=True, blank=True)
	description = HTMLField(null=True, blank=True)
	category = models.ForeignKey(Category, null=True, blank=True)
	author = models.ForeignKey(Author, null=True, blank=True)
	tags = TaggableManager()
	views = models.IntegerField(default=0)
	is_publish = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	image = models.FileField(upload_to=get_file_path, null=True, blank=True)

	def __unicode__(self):
		return self.title

	def save(self, *args, **kwargs):
		if self.title:
			self.slug = slugify(self.title)
		super(Post, self).save(*args, **kwargs)
