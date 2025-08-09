from django.conf.urls import include, url
from . import views

app_name = 'Vision'

urlpatterns = [
    url(r'VisionIndex/', views.VisionIndex,name='VisionIndex'),
    url(r'VisionContent/(\d+)/', views.VisionContent,name='VisionContent'),  
    url(r'GetVisionnextpage/', views.GetVisionnextpage,name='GetVisionnextpage'),  
    
    url(r'login_vision/', views.login_vision,name='login_vision'),  
    url(r'logout_func/', views.logout_func,name='logout_func'),  
    url(r'signup_vision/', views.signup_vision,name='signup_vision'),  
    
    url(r'delcommentvision/', views.delcommentvision,name='delcommentvision'),  
    url(r'commentvision/', views.commentvision,name='commentvision'),  
    url(r'sendcode/', views.sendcode,name='sendcode'),  
    url(r'verifycode/', views.verifycode,name='verifycode'),  
    
    
    
    
    
]