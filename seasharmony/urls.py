"""seasharmony URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

from app import views

urlpatterns = [
    path("", views.index),
    path('admin/', admin.site.urls),
    path('login/', views.login),
    path('createUser/', views.create_user),
    path('authTest/', views.auth_test),
    path('createMentor/', views.create_mentor),
    path('createMentee/', views.create_mentee),
    path('getFamily/', views.get_user_family),
    path('createFamilies/', views.create_families),
    path('getAllFamilies/', views.get_all_families),
    path('hasCompletedProfile/', views.has_completed_profile),
    path('isMentor/', views.is_mentor),
    path('logout/', views.logout),
    path('getCurrentUser/', views.get_current_user),
    path('populateUsers/', views.populate_users),
    path('requestResetPassword/', views.request_password_reset),
    path('resetPassword/', views.reset_password),
    path('clearPairings/', views.clear_pairings_database),
    path('getToken/', views.get_csrf_token)



]
