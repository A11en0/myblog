"""myblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, re_path, include
from blog.views import *
from django.conf import settings
from django.views.static import serve
from blog.upload import upload_image
from django.conf.urls import handler404, handler500

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r"^uploads/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT, }),
    re_path(r'^admin/upload/(?P<dir_name>[^/]+)$', upload_image, name='upload_image'),
    re_path('', include('blog.urls')),
    re_path(r'^comment/post/$', comment_post, name='comment_post'),
    re_path(r'^logout$', do_logout, name='logout'),
    re_path(r'^reg', do_reg, name='reg'),
    re_path(r'^login', do_login, name='login'),
   ] 

