from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render,HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
from bifrost.models import *
from django.contrib.auth.models import User
import math
from django.core.mail import send_mail
import random
import string
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth.hashers import make_password

# Create your views here.
# 用于同时使用用户名或邮箱登陆的功能重写
# class MyBackend(ModelBackend):
#     def authenticate(self, request, username, password, **kwargs):
#         try:
#             user = User.objects.get(Q(username=username)|Q(email=username)) # 如果还要用手机登陆，就加入| Q(mobile=username)
#             if user.check_password(password):   # 加密明文密码
#                 return user
#         except Exception as e:
#             print(e)
#             print('行号', e.__traceback__.tb_lineno)
#             return None

def BlogIndex(request):
    # 获取所有的列表
    all_bldata = Blogs.objects.filter(blog_status='open').values()
    all_bldata = list(all_bldata)
    for i in all_bldata:
        i['create_time'] = i['create_time'].strftime("%B-%d")

    bldata_len = math.ceil( len(all_bldata) / 10) # 获取总页数

    page = request.GET.get('page')# 获取分页数
    paginator = Paginator(all_bldata,10) #每一页10篇文章
    page_num=paginator.num_pages #总页数
    try:
        bldata = paginator.page(page)
    except PageNotAnInteger:
        bldata = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        bldata = paginator.page(paginator.num_pages)
    return render(request,'BlogIndex.html', locals())

# @login_required(login_url='/login/')
def BlogContent(request,blogID):
    try:
        data = Blogs.objects.filter(ID=blogID).values()
        data = list(data)[0]
        # 默认0开始
        blogid = data['ID']
        blogname = data['blog_title']
        blogcontent = data['blog_content']

        # 获得评论
        comdata = BlogComment.objects.filter(BlogID=blogID).values()
        comdata = list(comdata)[::-1]
        com_len = len(comdata)

        ContentData = {
            'blogid': blogid,
            'blogname': blogname,
            'blogcontent': blogcontent,
            'comdata':comdata,
            'com_len':com_len
        }
        return render(request,'BlogContent.html',{'contdata':ContentData})
    except Exception as e:
        print(e)
        print('行号', e.__traceback__.tb_lineno)

def login_blog(request):
    try:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            if username is not None and password is not None:
                # 如果是邮箱，将username改为查询
                if '@' in username and '.' in username:
                    username = User.objects.get(email=username)
                else:
                    pass
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    info = {
                        'res':'suc',
                        'suc_message': '登陆成功'
                    }
                    return HttpResponse(json.dumps(info))
                else:
                    info = {
                        'res':'error',
                        'error_message':"Invalid username or password."
                    }
                    return HttpResponse(json.dumps(info))
            else:
                info = {
                    'res':'error',
                    'error_message':"Invalid username or password."
                }
                return HttpResponse(json.dumps(info))
                
        else:
            return render(request, 'login.html')
    except Exception as e:
        print(e)
        print('行号', e.__traceback__.tb_lineno)
        raise

def signup_blog(request):
    try:
        userinfo = request.POST
        username = userinfo['username']
        mailaddr = userinfo['mailaddr']
        pwd = userinfo['password']
        if User.objects.filter(username=username).exists():
            rginfo = {
                'res': 'error_name_isexist'
            }
            return HttpResponse(json.dumps(rginfo))
        elif User.objects.filter(email=mailaddr).exists():
            rginfo = {
                'res': 'error_mail_isexist'
            }
            return HttpResponse(json.dumps(rginfo))
        else:
            User.objects.create_user(
                username = username,\
                email = mailaddr,\
                password = pwd
            )
            rginfo = {
                'res': 'suc'
            }
            return HttpResponse(json.dumps(rginfo))
    except Exception as e:
        print(e)
        print('行号', e.__traceback__.tb_lineno)
        raise

def sendcode(request):
    try:
        info = request.POST
        recordmailaddr = info['recordmailaddr']

        # 判断邮箱是否存在
        if User.objects.filter(email=recordmailaddr).exists():
            cl = [0,1,2,3,4,5,6,7,8,9]
            code = str(random.choice(cl))+str(random.choice(cl))+str(random.choice(cl))+str(random.choice(cl))
            
            email_title = '密码找回'
            email_body = 'Code: %s' %code
            send_mail(
                email_title,
                email_body,
                'postmaster@ladder3.cn',
                [recordmailaddr],
            )
            VerifyMailRecord.objects.create(
                MailAddr = recordmailaddr,\
                Code = code
            )
            return HttpResponse(200)
        else:
            return HttpResponse(500)

    except Exception as e:
        print(e)
        print('行号', e.__traceback__.tb_lineno)
        raise

def verifycode(request):
    try:
        info = request.POST
        recordmailaddr = info['recordmailaddr']
        recordcode = info['recordcode']
        ReinputPassword = info['ReinputPassword']

        # 获取最后一次邮箱的验证码
        mailinfo = VerifyMailRecord.objects.filter(MailAddr=recordmailaddr).values()
        mailinfo = list(mailinfo)[-1]['Code']
        if str(recordcode) == str(mailinfo):
            user = User.objects.filter(email=recordmailaddr).values()
            User.objects.filter(email=recordmailaddr).update(password=make_password(ReinputPassword))
            resinfo = {
                'res': 'suc',
                'recordcode': recordcode
            }
            return HttpResponse(json.dumps(resinfo))
        else:
            resinfo = {
                'res': 'error',
                'recordcode': recordcode
            }
            return HttpResponse(json.dumps(resinfo))

    except Exception as e:
        print(e)
        print('行号', e.__traceback__.tb_lineno)
        raise


def commentblog(request):
    try:
        data = request.POST
        blogid = data['blogid']
        com_body = data['com_body']
        UserName = request.user

        blogcom = BlogComment.objects.create(
            BlogID = blogid,
            UserName = UserName,
            CommentBody = com_body
        )
        
        # 这里为了实时刷新页面，需要查询创建时间
        com_time = blogcom.create_time
        com_id = blogcom.ID
        cominfo = {
            'UserName': str(UserName),
            'com_time' : com_time.strftime("%Y-%m-%d %H:%M:%S"),
            'com_id': com_id
        }
        return HttpResponse(json.dumps(cominfo))
    except Exception as e:
        print(e)
        print('行号', e.__traceback__.tb_lineno)
        raise

def delcommentblog(request):
    try:
        data = request.POST
        blogcomID = data['blogcomID']
        BlogComment.objects.filter(ID=blogcomID).delete()
        
        cominfo = {
            'res': 'suc'
        }
        return HttpResponse(json.dumps(cominfo))
    except Exception as e:
        print(e)
        print('行号', e.__traceback__.tb_lineno)
        raise


def logout_func(request):
    logout(request)
    return HttpResponse(200)

def GetBlognextpage(request):
    try:
        data = request.POST
        blogalldata = Blogs.objects.all()
        blogid = data['blogid']

        # 判断
        if int(blogid) == len(blogalldata):
            blognextid = 0
            nextblog_title = 0
            nextblog_describe = 0
        else:
            blognextid = int(data['blogid']) + 1
            # 最大循环所有blog的数量
            for i in range(len(blogalldata)):
                blognextdata = Blogs.objects.filter(ID=blognextid).values()
                blognextdata = list(blognextdata)
                if blognextdata[0]['blog_status']=='open':
                    # 如果open，定义数据
                    nextblog_title = blognextdata[0]['blog_title']
                    nextblog_describe = blognextdata[0]['blog_describe']
                else:
                    blognextid += 1

        if int(blogid) == 1:
            blogpreid = 0
            preblog_title = 0
            preblog_describe = 0

        else:
            blogpreid = int(data['blogid']) - 1
            for i in range(len(blogalldata)):
                blogpredata = Blogs.objects.filter(ID=blogpreid).values()
                blogpredata = list(blogpredata)
                if blogpredata[0]['blog_status']=='open':
                    # 如果open，定义数据
                    preblog_title = blogpredata[0]['blog_title']
                    preblog_describe = blogpredata[0]['blog_describe']
                else:
                    blogpreid -= 1
        
        
        datalist = {
            "blogpreid": blogpreid,
            "preblog_title": preblog_title,
            "preblog_describe": preblog_describe,
            "blognextid": blognextid,
            "nextblog_title": nextblog_title,
            "nextblog_describe": nextblog_describe,
        }
        return HttpResponse(json.dumps(datalist))
    except Exception as e:
        print(e)
        print('行号', e.__traceback__.tb_lineno)
        raise


