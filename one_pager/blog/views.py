from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import Post, Testemonial

class PostListView(ListView):
    model = Post
    template_name = 'index.html'
    context_object_name = 'posts'
    ordering = ['-timestamp']
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)    
        context['posts'] = Post.objects.all()
        return context

class UserPostListView(ListView):
    model = Post
    template_name = 'user_posts.html'
    context_object_name = 'posts'
    paginate_by = 3
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)    
        context['posts'] = Post.objects.all()
        return context

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-timestamp')

class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post_form.html'
    fields = ['title', 'content', 'post_image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'post_form.html'
    fields = ['title', 'content', 'post_image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    template_name = 'post_confirm_delete.html'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class TestemonialListView(ListView):
    model = Testemonial
    template_name = 'base.html'
    context_object_name = 'testemonials'
    ordering = ['-timestamp']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)    
        context['testemonials'] = Testemonial.objects.all()
        return context

class TestemonialDetailView(DetailView):
    model = Testemonial
    template_name = 'testemonial_detail.html'

class TestemonialCreateView(LoginRequiredMixin, CreateView):
    model = Testemonial
    template_name = 'testemonial_form.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
        
class TestemonialUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Testemonial
    template_name = 'testemonial_form.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        testemonial = self.get_object()
        if self.request.user == testemonial.author:
            return True
        return False

class TestemonialDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Testemonial
    success_url = '/'
    template_name = 'testemonial_confirm_delete.html'

    def test_func(self):
        testemonial = self.get_object()
        if self.request.user == testemonial.author:
            return True
        return False