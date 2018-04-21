from django.urls import re_path
from blog.views import *
from django.conf.urls import handler404, handler500

urlpatterns = [
    re_path(r'^$', index, name='index'),
   # re_path('^archive/$', archive, name='archive'),
   #re_path(r'^comment/post/$', comment_post, name='comment_post'),
    re_path(r'^article/$', article, name='article'),
    re_path(r'^blog/$', blog, name='blog'),
    re_path(r'^about/$', about, name='about'),
]


handler500=page_error
handler404=page_not_found
