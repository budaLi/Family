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
    url('^index/$',views.index,name="index"),
    url('^ad_index/$',views.ad_index,name="ad_index"),
    url('^ad_login/$',views.ad_login,name="ad_login"),
    url('^user_list/$',views.user_list,name="user_list"),
    url('^user_view/(\d+)/$',views.user_view,name="user_view"),
    url('^user_login/$',views.user_login,name="user_login"),
    url('^user_register/$',views.user_register,name="user_register"),
    url("^relation/$",views.relation,name="relation"),
    url("^tree/$",views.tree,name="tree"),
    url("^editperson/$",views.editperson,name="editperson"),
    url("^oplog_list/$",views.oplog_list,name="oplog_list"),
    url("^adminloginlog_list/$",views.adminloginlog_list,name="adminloginlog_list"),
    url("^userloginlog_list/$",views.userloginlog_list,name="userloginlog_list"),
    url("^auth_add/$",views.auth_add,name="auth_add"),
    url("^auth_list/$",views.auth_list,name="auth_list"),
    url("^role_add/$",views.role_add,name="role_add"),
    url("^role_list/$",views.role_list,name="role_list"),
    url("^admin_add/$",views.admin_add,name="admin_add"),
    url("^admin_list/$",views.admin_list,name="admin_list"),
      # path('^admin/', admin.site.urls),
]
