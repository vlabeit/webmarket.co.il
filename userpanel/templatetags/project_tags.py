from datetime import timedelta, timezone
import datetime
from tokenize import Number
from urllib import request
from django import template

from oscar.core.utils import format_timedelta

register = template.Library()
from oscar.apps.order.models import Order as OrderProduct
from oscar.apps.order.models import Line as  LineProduct
from ..models import Projects, AddOns

@register.simple_tag
def total_projects():
    return Projects.objects.count()

@register.filter
def index(sequence, position):
    return sequence[position]

@register.simple_tag
def add_to_addons(*args, **kwargs):
    AddOns.objects.create(user_id='user', name='ssrrrdsa', project='10.2', product= 'dasd')

@register.filter
def get_old_price(price):
    oldprice = int(price) * 1.2
    return oldprice

@register.simple_tag
def active_projects(user, *args, **kwargs):
    return len(Projects.objects.filter(user_email=user, is_active=True))

@register.simple_tag
def active_products(user, *args, **kwargs):
    return len(OrderProduct.objects.filter(user=user))

@register.filter
def time_left_subs(startime):
    started  = datetime.datetime.now(timezone.utc) - startime
    dateint = started.days
    percent = dateint/365*100
    return f"{percent:10.0f}"

@register.filter
def addonname(allnames):
    for num in range(len(allnames)):
        addonz = allnames[:num]
        
    # number_of_addons = int(len(allnames))
    # for add in range(number_of_addons):
    #     addonz = allnames[:add]
    # add+=1
    return addonz


@register.simple_tag
def allproducts(user, *args, **kwargs):
    orderlist,linelist,productlist =[],[],[]
    newlist =[]
    orders = OrderProduct.objects.filter(user=user)
    # order_order = orders.get('order')
    lines = LineProduct.objects.all()
    for line in lines:
        linelist.append(line.order)
    for order in orders:
        orderlist.append(order)

    for linez in linelist:
        if linez in orderlist:
            # print(linez)
            # productlist.append(linez) 
            final_product = LineProduct.objects.filter(order=linez)
    for pro in final_product:
        if pro in newlist:
            pass
        else:
            newlist.append(pro.title)
    print(f"{len(newlist)} number")

    return newlist
    
      