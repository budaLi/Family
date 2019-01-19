"""Family URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url
from app import views
urlpatterns = [
    path('admin/', admin.site.urls),
    url('^index/',views.index,name="index"),
    url('^admin_index/',views.admin_index,name="admin_index"),
    url('^admin_login/',views.admin_login,name="admin_login"),
    url('^user_list/',views.user_list,name="user_list"),
    url('^user_view/',views.user_view,name="user_view"),
    url('^user_login/',views.user_login,name="user_login"),
    url('^user_register/',views.user_register,name="user_register"),
    url("^relation/",views.relation,name="relation"),
]
