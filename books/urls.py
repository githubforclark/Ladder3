from django.conf.urls import include, url
from . import views

app_name = 'BookStacks'

urlpatterns = [
    url(r'Stacks', views.Stacks,name='Stacks'),
    url(r'Books/(\d+)/', views.BooksContent,name='BooksContent'),  
    url(r'GetBooknextpage/', views.GetBooknextpage,name='GetBooknextpage'),  
    url(r'login_bookstacks/', views.login_bookstacks,name='login_bookstacks'),  
    url(r'logout_func/', views.logout_func,name='logout_func'), 
    url(r'signup_bookstacks/', views.signup_bookstacks,name='signup_bookstacks'), 
    url(r'sendcode/', views.sendcode,name='sendcode'), 
    url(r'verifycode/', views.verifycode,name='verifycode'), 
    url(r'commentbookstacks/', views.commentbookstacks,name='commentbookstacks'), 
    url(r'delcommentbook/', views.delcommentbook,name='delcommentbook'), 

]