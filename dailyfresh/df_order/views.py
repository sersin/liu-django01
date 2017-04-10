#coding=utf-8
from django.http import HttpResponse
from django.shortcuts import render,redirect
from df_user import user_decorator
from df_user.models import UserInfo
from df_cart.models import *
from django.db import transaction
from models import *
from datetime import datetime
from decimal import Decimal

@user_decorator.login
def order(request):
    #通过id查找用户
    user = UserInfo.objects.get(id=request.session['user_id'])
    #通过购物车提交的get查询用户购买信息
    get = request.GET
    cart_ids = get.getlist('cart_id')
    cart_ids1 = [int(item) for item in cart_ids]
    carts = CartInfo.objects.filter(id__in=cart_ids1)

    context = {'carts':carts,'user':user,'cart_ids':','.join(cart_ids)}
    return render(request,'df_order/place_order.html',context)

@transaction.atomic()
@user_decorator.login
def order_handle(request):
    tran_id = transaction.savepoint()
    cart_ids = request.POST.get('cart_ids')

    try:
        order = OrderInfo()
        now = datetime.now()
        uid = request.session['user_id']
        order.oid = '%s%d'%(now.strftime('%Y%m%d%H%M%S'),uid)
        order.user_id = uid
        order.odate = now
        order.ototal = Decimal(request.POST.get('total'))
        order.oaddress = request.POST.get('address')
        order.save()

        cart_ids1 = [int(item) for item in cart_ids.split(',')]
        for id1 in cart_ids1:
            detail = OrderDetailInfo()
            detail.order = order

            cart = CartInfo.objects.get(id=id1)

            goods = cart.goods
            if goods.gkucun >= cart.count:
                goods.gkucun = goods.gkucun - cart.count
                goods.save()

                detail.goods_id = goods.id
                detail.price = goods.gprice
                detail.count = cart.count
                detail.save()

                cart.delete()
            else:
                transaction.savepoint_rollback(tran_id)
                return redirect('/cart/')
        transaction.savepoint_commit(tran_id)
    except Exception as e:
        print '================%s'%e
        transaction.savepoint_rollback(tran_id)
    return redirect('/user_center_order/')

@user_decorator.login
def pay(request,oid):
    order = OrderInfo.objects.get(oid=oid)
    order.oIsPay = True
    order.save()
    context={
        'order':order
    }
    return render(request,'df_order/pay.html',context)
















