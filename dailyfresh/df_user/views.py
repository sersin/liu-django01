#coding=utf-8
from django.shortcuts import render,redirect
from models import *
from hashlib import sha1
from django.http import JsonResponse,HttpResponseRedirect
from . import user_decorator
from df_goods.models import *
from df_order.models import *
from django.core.paginator import Paginator,Page

def register(request):
    return render(request,'df_user/register.html')

def register_handle(request):
    # 接收用户输入
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    upwd2 = post.get('cpwd')
    uemail = post.get('email')
    # 判断两次密码
    if upwd!=upwd2:
        return redirect('/register/')
    # 判断用户名是否存在
    i = UserInfo.objects.filter(uname = uname)
    if len(i) != 0:
        return redirect('/register/')
    # 给密码加密
    s1 = sha1()
    s1.update(upwd)
    upwd3 = s1.hexdigest()
    # 把数据保存到数据库
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd3
    user.uemail = uemail
    user.save()
    #注册成功跳转登陆页面
    return redirect('/login/')

def register_exist(request):
    uname = request.GET.get('uname')
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count':count})

def login(request):
    uname = request.COOKIES.get('uname')
    context = {'uname':uname,'error_name': 0,'error_pwd': 0}
    return render(request,'df_user/login.html',context)

def login_handle(request):
    post = request.POST
    put_name = post.get('username')
    put_pwd = post.get('pwd')
    jizhu = post.get('jizhu', 0)

    list = UserInfo.objects.filter(uname=put_name)

    if len(list) == 1:
        s1 = sha1()
        s1.update(put_pwd)
        if s1.hexdigest() == list[0].upwd:
            url = request.COOKIES.get('url', '/goods')
            red = HttpResponseRedirect(url)
            if jizhu != 0:
                red.set_cookie('uname',put_name)
            else:
                red.set_cookie('uname','',max_age=-1)
            request.session['user_id']=list[0].id
            request.session['user_name']=put_name
            return red
        else:
            context = {'error_name': 0,'error_pwd': 1,'uname':put_name,'upwd':put_pwd}
        return render(request,'df_user/login.html',context)
    else:
        context = {'error_name': 1,'error_pwd': 0,'uname':put_name,'upwd':put_pwd}
        return render(request, 'df_user/login.html', context)

def logout(request):
    request.session.flush()
    return redirect('/goods/')

@user_decorator.login
def user_center_info(request):
    user_email = UserInfo.objects.get(id=request.session['user_id']).uemail
    user_address = UserInfo.objects.get(id=request.session['user_id']).uaddress

    goods_ids = request.COOKIES.get('goods_ids','')
    goods_list = []
    if goods_ids != '':
        goods_ids1 = goods_ids.split(',')
        for goods_id in goods_ids1:
            goods_list.append(GoodsInfo.objects.get(id=int(goods_id)))

    context = {
        'user_name':request.session['user_name'],
        'user_email':user_email,
        'goods_list':goods_list,
        'user_address':user_address,
               }
    print user_email,request.session['user_name']
    return render(request,'df_user/user_center_info.html',context)

@user_decorator.login
def user_center_order(request,pindex):
    uid = request.session['user_id']
    order_list = OrderInfo.objects.filter(user_id=uid).order_by('-oid')
    paginator = Paginator(order_list,2)
    if pindex == '':
        pindex = '1'
    page = paginator.page(int(pindex))

    context = {
        'paginator':paginator,
        'page':page,
    }
    return render(request,'df_user/user_center_order.html',context)

@user_decorator.login
def user_center_site(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    if request.method=='POST':
        post=request.POST
        user.ushou=post.get('ushou')
        user.uaddress=post.get('uaddress')
        # print(post.get('uaddress'))
        user.uyoubian=post.get('uyoubian')
        user.uphone=post.get('uphone')
        user.save()
    context = {'user':user}
    return render(request,'df_user/user_center_site.html',context)







































