#coding=utf8
from django.shortcuts import render,render_to_response
from django import forms
from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate,login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import User,Passage
from django.http import JsonResponse

# Create your views here.

def login_view(request):
    """登录页面"""
    if request.method == "POST":
        uf = UserFormLogin(request.POST)
        if uf.is_valid():
            #获取表单信息
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username,password=password)

            if user is not None:   #如果用户存在
                if user.is_active:  #如果用户没有销户
                    global USERNAME
                    USERNAME = username
                    login(request,user)
                    return HttpResponseRedirect("/home.html/")
                else:
                    error="该用户已经注销"
                    return render(request, "userlogin.html",{'error': error})
            else:
                error = "用户名或密码错误"
                return render(request, "userlogin.html", {'error': error})
    else:
        uf = UserFormLogin()
    return render(request,"userlogin.html")


def register(request):
    #curtime=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime());
    """注册"""
    if request.method == "POST":
        uf = UserForm(request.POST)
        if uf.is_valid():
            #获取表单信息
            username = uf.cleaned_data['username']
            filterResult = User.objects.filter(username = username)
            if len(filterResult)>0:
                return render(request,'Register.html',{"errors":"用户名已存在"})
            else:
                password1 = uf.cleaned_data['password1']
                password2 = uf.cleaned_data['password2']
                if (password2 != password1):
                    return render(request,'Register.html',{'errors':"两次输入的密码不一致!"})
            #将表单写入数据库
                #password = password2
                user = User.objects.create_user(username=username,password=password1)
                user.save()
            #返回注册成功页面
                return HttpResponseRedirect("/login_view/")
    return render(request,'Register.html')

@login_required  #如果用户未认证，则返回登录页面
def home(request):
    """主页面，显示照片和故事"""
    story = Passage.objects.order_by("-id")[0:8]
    return render(request, 'home.html', {'story': story})

@login_required  #如果用户未认证，则返回登录页面
def upload(request):
    """上传故事，照片"""
    if request.method=="POST":
        load = UpLoad(request.POST)
        load2 = UpLoad2(request.POST)
        if load.is_valid() or load2.is_valid():
            titlex = request.POST['title']
            passagex = request.POST['passage']
            imgx=request.FILES.get('img')
            up = Passage.objects.create(author=USERNAME,title=titlex, article=passagex,img=imgx)
            up.save()
            return HttpResponseRedirect("/home.html/")
    else:
        return render(request,'upload.html')

@login_required  #如果用户未认证，则返回登录页面
def user_info(request):
    """个人信息页面,如果提交表单，就修改信息"""

    if request.method=="POST":
        first_name = request.POST['first_name']
        sex = request.POST['sex']
        motto = request.POST['motto']
        photo = request.FILES.get('photo')
        info = User.objects.get(username=USERNAME)
        info.first_name = first_name
        info.sex = sex
        info.photo = photo
        info.motto = motto
        info.save()
        return render(request, "user_info.html", {'info': info})
    info = User.objects.get(username=USERNAME)
    return render(request,"user_info.html",{'info': info})

def logout_view(request):
    """登出用户"""
    logout(request)
    return HttpResponseRedirect("/login_view")



class UserForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=100)
    password1 = forms.CharField(label='密码',widget=forms.PasswordInput())
    password2 = forms.CharField(label='确认密码',widget=forms.PasswordInput())

class UserFormLogin(forms.Form):
    username = forms.CharField(label='用户名',max_length=100)
    password = forms.CharField(label='密码',widget=forms.PasswordInput())

class UpLoad(forms.Form):
    title = forms.CharField(label="标题",max_length=100)
    passage = forms.Textarea()
    img = forms.FileField()
class UpLoad2(forms.Form):
    title = forms.CharField(label="标题",max_length=100)
    passage = forms.Textarea()



