"""FirstProject URL Configuration

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
from django.contrib.auth import views as auth_views
from django.urls import path
from app import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.start_screen),
    #path('/', views.start_screen),
    path('admin/', admin.site.urls),
    path('feed/', views.feed),
    path('friends/', views.friends),
    path('profile/', views.profile),
    path('profile/edit/', views.edit_profile),
    path('create/', views.create),
    path('login/', auth_views.LoginView.as_view(template_name='login.html')),
    path('search/', views.search),
    path('comment/', views.comment),
    path('post_details/<int:post_id>', views.post_details),
    path('logout/', views.logout),
    path('register/', views.register),
    path('delete/', views.delete)
    # path('profile/<str:email>', )
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
