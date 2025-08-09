from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from bifrost.models import *
import json
# Create your views here.
# 管理界面
login_required(redirect_field_name='next')

@login_required
def blogctl(request):
    return render(request,'blogctl.html')

@login_required
def visionctl(request):
    return render(request,'visionctl.html')

@login_required
def bookctl(request):
    return render(request,'bookctl.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if username == 'clark_ladder3' and password is not None:
            # username 是你通过user表创建出来的,如果验证通过，使用login载入，转换路由
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                print(user)
                return render(request, 'blogctl.html')
            else:
                error_message = "Invalid username or password."
                return render(request, 'login.html', {'error_message': error_message})
        else:
            error_message = "Invalid username or password."
            return render(request, 'login.html', {'error_message': error_message})
            
    else:
        return render(request, 'login.html')

    
def GetBlogList(request):
    try:
        data = Blogs.objects.all().values()
        data = list(data)[::-1]
        for i in data:
            i['create_time'] = i['create_time'].strftime("%Y-%m-%d")
            i['update_time'] = i['update_time'].strftime("%Y-%m-%d")

        datalist = {
            "bloglist": data,
        }
        return HttpResponse(json.dumps(datalist))
    except Exception as e:
        print(e)
        print('行号', e.__traceback__.tb_lineno)
        raise
def GetVisionList(request):
    try:
        data = Visions.objects.all().values()
        data = list(data)[::-1]
        for i in data:
            i['create_time'] = i['create_time'].strftime("%Y-%m-%d")
            i['update_time'] = i['update_time'].strftime("%Y-%m-%d")

        datalist = {
            "visionslist": data,
        }
        return HttpResponse(json.dumps(datalist))
    except Exception as e:
        print(e)
        print('行号', e.__traceback__.tb_lineno)
        raise
def GetBookList(request):
    try:
        data = Books.objects.all().values()
        data = list(data)[::-1]
        for i in data:
            i['create_time'] = i['create_time'].strftime("%Y-%m-%d")
            i['update_time'] = i['update_time'].strftime("%Y-%m-%d")

        datalist = {
            "booklist": data,
        }
        return HttpResponse(json.dumps(datalist))
    except Exception as e:
        print(e)
        print('行号', e.__traceback__.tb_lineno)
        raise


def AddBlogs(request):
    data = request.POST
    blog_title = data['blog_title']
    blog_describe = data['blog_describe']
    blog_imglink = data['blog_imglink']
    blog_content = data['blog_content']
    
    Blogs.objects.create(
        blog_title = blog_title,\
        blog_describe = blog_describe,\
        blog_content = blog_content,\
        blog_imglink = blog_imglink,\
        blog_status = 'open'
    )
    return HttpResponse(200)

def AddVisions(request):
    try:
        data = request.POST
        vs_title = data['vs_title']
        vs_describe = data['vs_describe']
        vs_imglink = data['vs_imglink']
        vision_jumbo_title = data['vision_jumbo_title']
        vision_jumbo_space = data['vision_jumbo_space']
        vision_jumbo_imglink = data['vision_jumbo_imglink']
        
        vs_content = data['vs_content']
        
        Visions.objects.create(
            vision_title = vs_title,\
            vision_describe = vs_describe,\
            vision_content = vs_content,\
            vision_imglink = vs_imglink,\
            book_jumbo_title = vision_jumbo_title,\
            book_jumbo_space = vision_jumbo_space,\
            book_jumbo_imglink = vision_jumbo_imglink,\
            vision_status = 'open'
        )
        return HttpResponse(200)
    except Exception as e:
        print(e)
        print('行号', e.__traceback__.tb_lineno)
        raise

def AddBooks(request):
    data = request.POST
    book_title = data['book_title']
    book_describe = data['book_describe']
    book_imglink = data['book_imglink']
    book_jumbo_title = data['book_jumbo_title']
    book_jumbo_space = data['book_jumbo_space']
    book_jumbo_imglink = data['book_jumbo_imglink']

    book_content = data['book_content']

    Books.objects.create(
        book_title = book_title,\
        book_describe = book_describe,\
        book_content = book_content,\
        book_imglink = book_imglink,\
        book_jumbo_title = book_jumbo_title,\
        book_jumbo_space = book_jumbo_space,\
        book_jumbo_imglink = book_jumbo_imglink,\
        
        book_status = 'open'
    )
    return HttpResponse(200)

def ChangeBlogState(request):
    data = request.POST
    blog_id = data['blog_id']
    blog_data = Blogs.objects.filter(ID=blog_id).values()
    blog_data = list(blog_data)[0]
    if blog_data['blog_status'] == 'open':
        status = 'close'
        Blogs.objects.filter(ID=blog_id).update(blog_status=status)
        blog_info = {
            'blog_id': blog_id,
            'blog_status': status
        }
        return HttpResponse(json.dumps(blog_info))

    elif blog_data['blog_status'] == 'close':
        status = 'open'
        Blogs.objects.filter(ID=blog_id).update(blog_status=status)
        blog_info = {
            'blog_id': blog_id,
            'blog_status': status
        }
        return HttpResponse(json.dumps(blog_info))
    
def ChangeVisionState(request):
    data = request.POST
    vision_id = data['vision_id']
    vision_data = Visions.objects.filter(ID=vision_id).values()
    vision_data = list(vision_data)[0]
    if vision_data['vision_status'] == 'open':
        status = 'close'
        Visions.objects.filter(ID=vision_id).update(vision_status=status)
        book_info = {
            'vision_id': vision_id,
            'vision_data': status
        }
        return HttpResponse(json.dumps(book_info))

    elif vision_data['vision_status'] == 'close':
        status = 'open'
        Visions.objects.filter(ID=vision_id).update(vision_status=status)
        book_info = {
            'vision_id': vision_id,
            'vision_data': status
        }
        return HttpResponse(json.dumps(book_info))
    
def ChangeBooksState(request):
    data = request.POST
    book_id = data['book_id']
    book_data = Books.objects.filter(ID=book_id).values()
    book_data = list(book_data)[0]
    if book_data['book_status'] == 'open':
        status = 'close'
        Books.objects.filter(ID=book_id).update(book_status=status)
        book_info = {
            'book_id': book_id,
            'book_data': status
        }
        return HttpResponse(json.dumps(book_info))

    elif book_data['book_status'] == 'close':
        status = 'open'
        Books.objects.filter(ID=book_id).update(book_status=status)
        book_info = {
            'book_id': book_id,
            'book_data': status
        }
        return HttpResponse(json.dumps(book_info))

# 编辑 blog
def EditBlogShow(request):
    try:
        data = request.POST
        blog_id = data['blog_id']
        blog_data = Blogs.objects.filter(ID=blog_id).values()
        blog_data = list(blog_data)[0]
        blog_data['create_time'] = blog_data['create_time'].strftime("%Y-%m-%d")
        blog_data['update_time'] = blog_data['update_time'].strftime("%Y-%m-%d")
        
        blog_info = {
            'blog_data': blog_data
        }
        return HttpResponse(json.dumps(blog_info))
    except Exception as e:
        print(e)
        print('行号', e.__traceback__.tb_lineno)
        raise
    
def EditBlog(request):
    data = request.POST
    blog_id = data['blog_id']
    blog_content = data['blog_content']
    blog_title = data['blog_title']
    blog_describe = data['blog_describe']
    blog_imglink = data['blog_imglink']

    Blogs.objects.filter(ID=blog_id).update(
        blog_title=blog_title,
        blog_describe=blog_describe,
        blog_imglink=blog_imglink,
        blog_content=blog_content
    )
    return HttpResponse(200)

# 编辑 vision
def EditVisionShow(request):
    try:
        data = request.POST
        vision_id = data['vision_id']
        vision_data = Visions.objects.filter(ID=vision_id).values()
        vision_data = list(vision_data)[0]
        vision_data['create_time'] = vision_data['create_time'].strftime("%Y-%m-%d")
        vision_data['update_time'] = vision_data['update_time'].strftime("%Y-%m-%d")
        
        vision_info = {
            'vision_data': vision_data
        }
        return HttpResponse(json.dumps(vision_info))
    except Exception as e:
        print(e)
        print('行号', e.__traceback__.tb_lineno)
        raise

def EditVision(request):
    data = request.POST
    vision_id = data['vision_id']
    vision_content = data['vision_content']
    vision_title = data['vision_title']
    vision_describe = data['vision_describe']
    vision_imglink = data['vision_imglink']
    vision_jumbo_title = data['vision_jumbo_title']
    vision_jumbo_space = data['vision_jumbo_space']
    vision_jumbo_imglink = data['vision_jumbo_imglink']
    

    Visions.objects.filter(ID=vision_id).update(
        vision_title=vision_title,
        vision_describe=vision_describe,
        vision_imglink=vision_imglink,
        vision_content=vision_content,
        vision_jumbo_title = vision_jumbo_title,\
        vision_jumbo_space = vision_jumbo_space,\
        vision_jumbo_imglink = vision_jumbo_imglink,\
    )
    return HttpResponse(200)

# 编辑 book
def EditBookShow(request):
    try:
        data = request.POST
        book_id = data['book_id']
        book_data = Books.objects.filter(ID=book_id).values()
        book_data = list(book_data)[0]
        book_data['create_time'] = book_data['create_time'].strftime("%Y-%m-%d")
        book_data['update_time'] = book_data['update_time'].strftime("%Y-%m-%d")
        
        book_info = {
            'book_data': book_data
        }
        return HttpResponse(json.dumps(book_info))
    except Exception as e:
        print(e)
        print('行号', e.__traceback__.tb_lineno)
        raise
def EditBook(request):
    data = request.POST
    book_id = data['book_id']
    book_content = data['book_content']
    book_title = data['book_title']
    book_describe = data['book_describe']
    book_imglink = data['book_imglink']
    book_jumbo_title = data['book_jumbo_title']
    book_jumbo_space = data['book_jumbo_space']
    book_jumbo_imglink = data['book_jumbo_imglink']
    

    Books.objects.filter(ID=book_id).update(
        book_title=book_title,
        book_describe=book_describe,
        book_imglink=book_imglink,
        book_content=book_content,
        book_jumbo_title=book_jumbo_title,
        book_jumbo_space=book_jumbo_space,
        book_jumbo_imglink=book_jumbo_imglink
    )
    return HttpResponse(200)



