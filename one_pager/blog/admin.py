from django.contrib import admin
from .models import Post, Testimonial, AudioFile, VideoFile
from audiofield.models import AudioFile as default
import os

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
	list_display = ('author', 'title', 'timestamp', 'slug')
	search_fields = ['title', 'content']

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
	list_display = ('author', 'title', 'timestamp')
	search_fields = ['title', 'content']

admin.site.unregister(default)

@admin.register(AudioFile)
class AudioFileAdmin(admin.ModelAdmin):
        list_display = ('header', 'is_checked', 'is_verified', 'checked_by', 'verified_by', 'checked_status', 'verified_status', 'timestamp')
        search_fields = ['header']
        list_filter = ('is_verified', 'checked_by', 'verified_by')
        actions = ['custom_delete_selected']
        
        def custom_delete_selected(self, request, queryset):
            #custom delete code
            n = queryset.count()
            for i in queryset:
                if i.audio_file:
                    if os.path.exists(i.audio_file.path):
                        os.remove(i.audio_file.path)
                i.delete()
            self.message_user(request, ("Successfully deleted %d audio files.") % n)
        custom_delete_selected.short_description = "Delete selected items"

        def get_actions(self, request):
            actions = super(AudioFileAdmin, self).get_actions(request)
            del actions['delete_selected']
            return actions

@admin.register(VideoFile)
class VideoFileAdmin(admin.ModelAdmin):
        list_display = ('header', 'timestamp') 
        search_fields = ['header']
        actions = ['custom_delete_selected']

        def custom_delete_selected(self, request, queryset):
            #custom delete code
            n = queryset.count()
            for i in queryset:
                if i.audio_file:
                    if os.path.exists(i.audio_file.path):
                        os.remove(i.audio_file.path)
                i.delete()
            self.message_user(request, ("Successfully deleted %d audio files.") % n)
        custom_delete_selected.short_description = "Delete selected items"

        def get_actions(self, request):
            actions = super(VideoFileAdmin, self).get_actions(request)
            del actions['delete_selected']
            return actions
