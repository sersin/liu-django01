#coding=utf-8
from django.shortcuts import render
from models import *
from django.core.paginator import Paginator
from df_cart.models import *

def index(request):
    typelist = TypeInfo.objects.all()

    fruit = typelist[0].goodsinfo_set.order_by('id')[0:4]
    fruit_hot = typelist[0].goodsinfo_set.order_by('-gclick')[0:3]
    seafood = typelist[1].goodsinfo_set.order_by('id')[0:4]
    seafood_hot = typelist[1].goodsinfo_set.order_by('-gclick')[0:3]
    meet = typelist[2].goodsinfo_set.order_by('id')[0:4]
    meet_hot = typelist[2].goodsinfo_set.order_by('-gclick')[0:3]
    egg = typelist[3].goodsinfo_set.order_by('id')[0:4]
    egg_hot = typelist[3].goodsinfo_set.order_by('-gclick')[0:3]
    vegetables = typelist[4].goodsinfo_set.order_by('id')[0:4]
    vegetables_hot = typelist[4].goodsinfo_set.order_by('-gclick')[0:3]
    ice = typelist[5].goodsinfo_set.order_by('id')[0:4]
    ice_hot = typelist[5].goodsinfo_set.order_by('-gclick')[0:3]

    context = {'fruit':fruit,'fruit_hot':fruit_hot,
               'seafood':seafood,'seafood_hot':seafood_hot,
               'meet':meet,'meet_hot':meet_hot,
               'egg':egg,'egg_hot':egg_hot,
               'vegetables':vegetables,'vegetables_hot':vegetables_hot,
               'ice':ice,'ice_hot':ice_hot,
               'cart_count': cart_count(request),
              }
    return render(request,'df_goods/index.html',context)

def list(request,tid,sort,pindex):
    typelist = TypeInfo.objects.get(pk=int(tid))
    news = typelist.goodsinfo_set.order_by('-id')[0:2]

    if sort == '1':
        goods_list = typelist.goodsinfo_set.order_by('-id')
    elif sort == '2':
        goods_list = typelist.goodsinfo_set.order_by('-gprice')
    elif sort == '3':
        goods_list = typelist.goodsinfo_set.order_by('gclick')

    paginator = Paginator(goods_list,10)
    page = paginator.page(int(pindex))

    context={
             'page':page,
             'paginator':paginator,
             'typelist':typelist,
             'sort':sort,
             'news':news,
             'cart_count':cart_count(request),
            }
    return render(request,'df_goods/list.html',context)

def detail(request, gid):
    goods = GoodsInfo.objects.get(pk=int(gid))
    type = goods.gtype.ttitle
    goods.gclick = goods.gclick + 1
    goods.save()
    news = goods.gtype.goodsinfo_set.order_by('-id')[0:2]
    context = {
        'goods':goods,
        'gid':gid,
        'news':news,
        'type':type,
        'cart_count': cart_count(request),
    }
    response = render(request,'df_goods/detail.html',context)

    goods_ids = request.COOKIES.get('goods_ids','')
    goods_id = '%d'%goods.id
    if goods_ids != '':
        goods_ids1 = goods_ids.split(',')
        if goods_ids1.count(goods_id) >= 1:
            goods_ids1.remove(goods_id)
        goods_ids1.insert(0,goods_id)

        if len(goods_ids1) >= 6:
            del goods_ids1[5]
        goods_ids = ','.join(goods_ids1)
    else:
        goods_ids = goods_id
    response.set_cookie('goods_ids',goods_ids)


    return response

def cart_count(request):
    if request.session.has_key('user_id'):
        return CartInfo.objects.filter(user_id=request.session['user_id']).count()
    else:
        return 0







