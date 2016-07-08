from django.contrib import admin
from mce_filebrowser.admin import MCEFilebrowserAdmin
from .models import Author, Category, Post

class PostAdmin(MCEFilebrowserAdmin):
	readonly_fields = ['views']
	list_display = ['title', 'category', 'author', 'views', 'is_publish']
	search_fields = ['title', 'description', 'author__name', 'category__name']
	list_filter = ['is_publish']

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
