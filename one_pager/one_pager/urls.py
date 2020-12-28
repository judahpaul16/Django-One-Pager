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

from blog.views import (
    HomeView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    PostDetailView,
    TestemonialCreateView,
    TestemonialUpdateView,
    TestemonialDeleteView
    )

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('post/<int:pk>/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<int:pk>/<slug:slug>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/<slug:slug>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('testemonial/<int:pk>/<slug:slug>/update/', TestemonialUpdateView.as_view(), name='testemonial-update'),
    path('testemonial/<int:pk>/<slug:slug>/delete/', TestemonialDeleteView.as_view(), name='testemonial-delete'),
    path('testemonial/new/', TestemonialCreateView.as_view(), name='testemonial-create'),
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
