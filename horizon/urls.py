from django.conf.urls import include, url
from . import views
from django.conf import settings
from django.views.static import serve

app_name = 'horizon'

urlpatterns = [
    url(r'', views.indexView,name='indexView'),
]
if not settings.DEBUG:
    urlpatterns += [url(r'^statics/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT})]
