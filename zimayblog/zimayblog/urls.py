"""
URL configuration for zimayblog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('app.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('courses/', views.courses, name='courses'),
    path('set-language/', views.set_language, name='set_language'),
    path('accounts/login/', views.UserLoginView.as_view(), name='login'),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/activate/<uidb64>/<token>/', views.activate_account, name='activate_account'),
    path('accounts/logout/', LogoutView.as_view(next_page="/"), name='logout'),
    path('diplomas/', views.diplomas, name='diplomas'),
    path('projects/', views.projects, name='projects'),
    path('projects/weather-live/', views.weather_project_live, name='weather_project_live'),
    path('projects/todo-live/', views.todo_project_live, name='todo_project_live'),
    path('about/', views.about, name='about'),
    path('project/', views.project, name='project'),
    path('gallery/', views.gallery, name='gallery'),
    path('contact/', views.contact, name='contact'),
    path('blog/', include('app.urls')),
]
