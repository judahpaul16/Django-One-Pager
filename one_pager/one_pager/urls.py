"""one_pager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from profiles import views as user_views
admin.autodiscover()

from blog.views import (
    HomeView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    PostDetailView,
    TestimonialCreateView,
    TestimonialUpdateView,
    TestimonialDeleteView,
    AudioFileAuditView,
    AudioListView,
    AudioDetailView,
    VideoListView,
    VideoDetailView,
    ArchiveView
    )

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('archive/', ArchiveView.as_view(), name='archive'),
    path('audit-audio/<int:pk>/', AudioFileAuditView.as_view(), name='audit-audio'),
    path('audio/', AudioListView.as_view(), name='audio'),
    path('audio/<int:pk>/', AudioDetailView.as_view(), name='audio-detail'),
    path('videos/', VideoListView.as_view(), name='videos'),
    path('videos/<int:pk>/', VideoDetailView.as_view(), name='video-detail'),
    path('post/<int:pk>/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/<slug:slug>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/<slug:slug>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('testimonial/update/', TestimonialUpdateView.as_view(), name='testimonial-update'),
    path('testimonial/delete/', TestimonialDeleteView.as_view(), name='testimonial-delete'),
    path('testimonial/new/', TestimonialCreateView.as_view(), name='testimonial-create'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('password-reset/',
        auth_views.PasswordResetView.as_view(template_name='password_reset.html'),
        name='password_reset'),
    path('password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
        name='password_reset_complete'),
    path('password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
        name='password_reset_confirm'),
    path('password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
        name='password_reset_done'),
    path('register/', user_views.register_view, name='register'),
    path('profile/', user_views.profile_view, name='profile'),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
