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
def Stacks(request):
    # 获取所有的列表
    all_boookdata = Books.objects.filter(book_status='open').values()
    all_boookdata = list(all_boookdata)

    bookdata_len = math.ceil( len(all_boookdata) / 10) # 获取总页数

    page = request.GET.get('page')# 获取分页数
    paginator = Paginator(all_boookdata,10) #每一页10篇文章
    page_num=paginator.num_pages #总页数
    try:
        bookdata = paginator.page(page)
    except PageNotAnInteger:
        bookdata = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        bookdata = paginator.page(paginator.num_pages)
    return render(request,'BookStacks.html', locals())

def BooksContent(request,bookID):
    try:
        data = Books.objects.filter(ID=bookID).values()
        data = list(data)[0]
        # 默认0开始
        bookid = data['ID']
        bookname = data['book_title']
        bookcontent = data['book_content']
        book_jumbo_imglink = data['book_jumbo_imglink']
        book_jumbo_title = data['book_jumbo_title']
        book_jumbo_space = data['book_jumbo_space']

        # 获取评论
        comdata = BookComment.objects.filter(BookID=bookid).values()
        comdata = list(comdata)[::-1]
        com_len = len(comdata)

        ContentData = {
            'bookid': bookid,
            'bookname': bookname,
            'bookcontent': bookcontent,
            'book_jumbo_imglink': book_jumbo_imglink,
            'book_jumbo_title': book_jumbo_title,
            'book_jumbo_space': book_jumbo_space,
            'comdata': comdata,
            'com_len': com_len
        }
        return render(request,'BooksContent.html',{'contdata':ContentData})
    except Exception as e:
        print(e)
        print('行号', e.__traceback__.tb_lineno)

def GetBooknextpage(request):
    try:
        data = request.POST
        bookalldata = Books.objects.all()
        bookid = data['bookid']

        # 判断，这个方法的缺陷是一旦数据库出现不连续的ID，例如删除某一篇文章，这个判断就失效
        if int(bookid) == len(bookalldata):
            booknextid = 0
            nextbook_title = 0
            nextbook_describe = 0
        else:
            booknextid = int(data['bookid']) + 1
            # 最大循环所有book的数量
            for i in range(len(bookalldata)):
                booknextdata = Books.objects.filter(ID=booknextid).values()
                booknextdata = list(booknextdata)
                if booknextdata[0]['book_status']=='open':
                    # 如果open，定义数据
                    nextbook_title = booknextdata[0]['book_title']
                    nextbook_describe = booknextdata[0]['book_describe']
                else:
                    booknextid += 1

        if int(bookid) == 1:
            bookpreid = 0
            prebook_title = 0
            prebook_describe = 0

        else:
            bookpreid = int(data['bookid']) - 1
            for i in range(len(bookalldata)):
                bookpredata = Books.objects.filter(ID=bookpreid).values()
                bookpredata = list(bookpredata)
                if bookpredata[0]['book_status']=='open':
                    # 如果open，定义数据
                    prebook_title = bookpredata[0]['book_title']
                    prebook_describe = bookpredata[0]['book_describe']
                else:
                    bookpreid -= 1
        
        
        datalist = {
            "bookpreid": bookpreid,
            "prebook_title": prebook_title,
            "prebook_describe": prebook_describe,
            "booknextid": booknextid,
            "nextbook_title": nextbook_title,
            "nextbook_describe": nextbook_describe,
        }
        return HttpResponse(json.dumps(datalist))
    except Exception as e:
        print(e)
        print('行号', e.__traceback__.tb_lineno)
        raise

#-------------------------------------------------------------
def login_bookstacks(request):
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

def signup_bookstacks(request):
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


def commentbookstacks(request):
    try:
        data = request.POST
        bookid = data['bookid']
        com_body = data['com_body']
        UserName = request.user

        bookcom = BookComment.objects.create(
            BookID = bookid,
            UserName = UserName,
            CommentBody = com_body
        )
        
        # 这里为了实时刷新页面，需要查询创建时间
        com_time = bookcom.create_time
        com_id = bookcom.ID
        cominfo = {
            'UserName': str(UserName),
            'com_id': com_id,
            'com_time' : com_time.strftime("%Y-%m-%d %H:%M:%S")
        }
        return HttpResponse(json.dumps(cominfo))
    except Exception as e:
        print(e)
        print('行号', e.__traceback__.tb_lineno)
        raise
def delcommentbook(request):
    try:
        data = request.POST
        bookcomID = data['bookcomID']
        BookComment.objects.filter(ID=bookcomID).delete()
        
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