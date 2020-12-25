from django.contrib import admin
from .models import Post, Testemonial

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ('author', 'title', 'timestamp', 'slug')
	search_fields = ['title', 'content']

@admin.register(Testemonial)
class TestemonialAdmin(admin.ModelAdmin):
	list_display = ('author', 'title', 'timestamp', 'slug')
	search_fields = ['title', 'content']