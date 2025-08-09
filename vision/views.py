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
def VisionIndex(request):
    # 获取所有的列表
    all_vidata = Visions.objects.filter(vision_status='open').values()
    all_vidata = list(all_vidata)

    vsdata_len = math.ceil( len(all_vidata) / 10) # 获取总页数

    page = request.GET.get('page')# 获取分页数
    paginator = Paginator(all_vidata,10) #每一页10篇文章
    page_num=paginator.num_pages #总页数
    try:
        vsdata = paginator.page(page)
    except PageNotAnInteger:
        vsdata = paginator.page(1)  # 如果用户输入的页码不是整数时,显示第1页的内容
    except EmptyPage:
        vsdata = paginator.page(paginator.num_pages)
    return render(request,'VisionIndex.html', locals())


def VisionContent(request,visID):
    data = Visions.objects.filter(ID=visID).values()
    data = list(data)[0]
    # 默认0开始
    vsid = data['ID']
    vstitle = data['vision_title']
    vscontent = data['vision_content']
    vision_jumbo_imglink = data['vision_jumbo_imglink']
    vision_jumbo_title = data['vision_jumbo_title']
    vision_jumbo_space = data['vision_jumbo_space']
    print(vision_jumbo_imglink)

    # 获取评论
    comdata = VisionComment.objects.filter(VisionID=vsid).values()
    comdata = list(comdata)[::-1]
    com_len = len(comdata)

    ContentData = {
        'visionid': vsid,
        'visionname': vstitle,
        'visioncontent': vscontent,
        'vision_jumbo_imglink': vision_jumbo_imglink,
        'vision_jumbo_title': vision_jumbo_title,
        'vision_jumbo_space': vision_jumbo_space,
        'comdata': comdata,
        'com_len': com_len
    }
    return render(request,'VisionContent.html',{'contdata':ContentData})

def GetVisionnextpage(request):
    try:
        data = request.POST
        visionalldata = Visions.objects.all()
        visionid = data['visionid']

        # 判断
        if int(visionid) == len(visionalldata):
            visionnextid = 0
            nextvision_title = 0
            nextvision_describe = 0
        else:
            visionnextid = int(data['visionid']) + 1
            # 最大循环所有blog的数量
            for i in range(len(visionalldata)):
                visionnextdata = Visions.objects.filter(ID=visionnextid).values()
                visionnextdata = list(visionnextdata)
                if visionnextdata[0]['vision_status']=='open':
                    # 如果open，定义数据
                    nextvision_title = visionnextdata[0]['vision_title']
                    nextvision_describe = visionnextdata[0]['vision_describe']
                else:
                    visionnextid += 1

        if int(visionid) == 1:
            visionpreid = 0
            prevision_title = 0
            prevision_describe = 0

        else:
            visionpreid = int(data['visionid']) - 1
            for i in range(len(visionalldata)):
                visionpredata = Visions.objects.filter(ID=visionpreid).values()
                visionpredata = list(visionpredata)
                if visionpredata[0]['vision_status']=='open':
                    # 如果open，定义数据
                    prevision_title = visionpredata[0]['vision_title']
                    prevision_describe = visionpredata[0]['vision_describe']
                else:
                    visionpreid -= 1
        
        
        datalist = {
            "visionpreid": visionpreid,
            "prevision_title": prevision_title,
            "prevision_describe": prevision_describe,
            "visionnextid": visionnextid,
            "nextvision_title": nextvision_title,
            "nextvision_describe": nextvision_describe,
        }
        return HttpResponse(json.dumps(datalist))
    except Exception as e:
        print(e)
        print('行号', e.__traceback__.tb_lineno)
        raise

#-------------------------------------------------------------
def login_vision(request):
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

def signup_vision(request):
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
            print(user)
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


def commentvision(request):
    try:
        data = request.POST
        visionid = data['visionid']
        com_body = data['com_body']
        UserName = request.user

        visioncom = VisionComment.objects.create(
            VisionID = visionid,
            UserName = UserName,
            CommentBody = com_body
        )
        
        # 这里为了实时刷新页面，需要查询创建时间
        com_time = visioncom.create_time
        com_id = visioncom.ID
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
def delcommentvision(request):
    try:
        data = request.POST
        visioncomID = data['visioncomID']
        VisionComment.objects.filter(ID=visioncomID).delete()
        
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