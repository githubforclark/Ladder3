from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'Bifrost'

urlpatterns = [
    url(r'accounts/login/$', views.login_view,name='login'),

    url(r'blogctl/', views.blogctl,name='blogctl'),
    url(r'AddBlogs/', views.AddBlogs,name='AddBlogs'),
    url(r'GetBlogList/', views.GetBlogList,name='GetBlogList'),
    url(r'ChangeBlogState/', views.ChangeBlogState,name='ChangeBlogState'),
    url(r'EditBlogShow/', views.EditBlogShow,name='EditBlogShow'),
    url(r'EditBlog/', views.EditBlog,name='EditBlog'),
    
    
    url(r'visionctl/', views.visionctl,name='visionctl'),
    url(r'AddVisions/', views.AddVisions,name='AddVisions'),
    url(r'GetVisionList/', views.GetVisionList,name='GetVisionList'),
    url(r'ChangeVisionState/', views.ChangeVisionState,name='ChangeVisionState'),
    url(r'EditVisionShow/', views.EditVisionShow,name='EditVisionShow'),
    url(r'EditVision/', views.EditVision,name='EditVision'),
    
    
    url(r'bookctl/', views.bookctl,name='bookctl'),
    url(r'AddBooks/', views.AddBooks,name='AddBooks'),
    url(r'GetBookList/', views.GetBookList,name='GetBookList'),
    url(r'ChangeBooksState/', views.ChangeBooksState,name='ChangeBooksState'),
    url(r'EditBookShow/', views.EditBookShow,name='EditBookShow'),
    url(r'EditBook/', views.EditBook,name='EditBook'),
    url(r'visionctl/', views.visionctl,name='visionctl'),
    url(r'blogctl/', views.blogctl,name='blogctl'),

]