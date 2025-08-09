from django.conf.urls import include, url
from . import views

app_name = 'Blog'

urlpatterns = [
    url(r'login/$', views.login_blog,name='login'),
    url(r'BlogIndex', views.BlogIndex,name='Blog'),
    url(r'BlogContent/(\d+)/', views.BlogContent,name='BlogContent'),
    url(r'GetBlognextpage/', views.GetBlognextpage,name='GetBlognextpage'),
    url(r'delcommentblog/', views.delcommentblog,name='delcommentblog'),
    url(r'commentblog/', views.commentblog,name='commentblog'),
    url(r'logout_func/', views.logout_func,name='logout_func'),
    url(r'signup/', views.signup_blog,name='signup_blog'),
    url(r'sendcode/', views.sendcode,name='sendcode'),
    url(r'verifycode/', views.verifycode,name='verifycode'),
    
    
]
#if not settings.DEBUG:
#    urlpatterns += [url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT})]
