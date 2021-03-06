"""tih_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from tih_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login),
    path('', views.home),
    path('home/', views.home),
    path('increase/', views.data_increase),
    path('delete/', views.delete_user),
    path('update/', views.data_update),
    path('display/', views.data_display),
    path('check/', views.date_check),
    path('burnin_result/<pindex>', views.burnin_data_display),
    path('burnin_result_check/<pindex>', views.burnin_data_search, name='burnin_data_search'),
]
