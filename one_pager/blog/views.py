from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from .models import Post, Testimonial, AudioFile, VideoFile
from django.contrib.sites.models import Site
from django.contrib import messages
from django.db import models
from django import forms
from .forms import AuditForm
from django.conf import settings
import requests
import certifi
import os

class HomeView(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'
    ordering = ['-timestamp']
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all()
        context['testimonials'] = Testimonial.objects.all()
        context['carousel_files'] = os.listdir(os.path.join(settings.STATIC_ROOT, "assets/images/carousel/"))
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post_form.html'
    fields = ['title', 'content', 'post_image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, f'Post successfully created!')
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'post_form.html'
    fields = ['title', 'content', 'post_image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, f'Post successfully updated!')
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author or self.request.user.is_superuser:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    template_name = 'post_confirm_delete.html'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author or self.request.user.is_superuser:
            return True
        return False

class TestimonialCreateView(LoginRequiredMixin, CreateView):
    model = Testimonial
    template_name = 'testimonial_form.html'
    fields = ['title', 'content']
    widgets = {
        'content' : forms.Textarea(attrs={
            'maxlength': '120',
        }),
    }

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, f'Testimonial successfully updated!')
        return super().form_valid(form)

class TestimonialUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Testimonial
    template_name = 'testimonial_form.html'
    fields = ['title', 'content']
    widgets = {
        'content' : forms.Textarea(attrs={
            'maxlength': '120',
        }),
    }

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, f'Testimonial successfully updated!')
        return super().form_valid(form)

    def test_func(self):
        testimonial = self.get_object()
        if self.request.user == testimonial.author or self.request.user.is_superuser:
            return True
        return False

class TestimonialDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Testimonial
    success_url = '/'
    template_name = 'testimonial_confirm_delete.html'

    def test_func(self):
        testimonial = self.get_object()
        if self.request.user == testimonial.author or self.request.user.is_superuser:
            return True
        return False

class AudioFileAuditView(LoginRequiredMixin, DetailView, FormView):
    model = AudioFile
    form_class = AuditForm
    template_name = 'audit-audio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['curr_audio_file'] = AudioFile.objects.get(pk=self.kwargs.get('pk'))
        context['audio_files'] = AudioFile.objects.all()
        return context

    def form_valid(self, form):
        messages.success(self.request, f'Audio file successfully audited!')
        return super().form_valid(form)

    def post(self, request, pk):
        form = self.get_form()
        result = request.POST.get("audit")
        nextpage = pk + 1
        domain = Site.objects.get_current().domain
        path = f"/audit-audio/{nextpage}/"
        self.success_url = path

        if form.is_valid():
            obj = AudioFile.objects.get(pk=pk)
            
            if not obj.is_checked:
                obj.checked_by = self.request.user
                obj.is_checked = True
                obj.checked_status = result
            elif not obj.is_verified:
                obj.verified_by = self.request.user
                obj.is_verified = True
                obj.verified_status = result
            
            obj.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form, **kwargs)

    def test_func(self):
        audiofile = self.get_object()
        if self.request.user == audiofile.checked_by or self.request.user == audiofile.verified_by:
            return False
        return True

class AudioListView(ListView):
    model = AudioFile
    template_name = 'audio.html'
    context_object_name = 'audio'
    ordering = ['-timestamp']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class AudioDetailView(DetailView):
    model = AudioFile
    template_name = 'audio_detail.html'
    context_object_name = 'audio'


class VideoListView(ListView):
    model = VideoFile
    template_name = 'videos.html'
    context_object_name = 'videos'
    ordering = ['-timestamp']
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class VideoDetailView(DetailView):
    model = VideoFile
    template_name = 'video_detail.html'
    context_object_name = 'video'

class ArchiveView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = VideoFile
    template_name = 'archive.html'
    
    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

