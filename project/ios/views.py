# coding=utf-8
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
import json

from conf import website

from database.models import bill

# Create your views here.


def get_method(request):
    name = request.GET['name']
    context = {
        'name': name,
        'age': '24',
    }

    return HttpResponse(json.dumps(context))


def post_method(request):
    name = request.POST['name']
    context = {
        'name': name,
        'age': '24',
    }

    return HttpResponse(json.dumps(context))


def showbill(request):
    bill_list = bill.objects.all()

    total = 0
    for item in bill_list:
        total += item.money

    context = {
        'bill_list': bill_list,
        'total': total
    }

    return render(request, website.bill, context)


def add(request):
    name = request.POST['name'].strip()
    money = int(request.POST['money'].strip())

    new_bill = bill.objects.create(
        name = name,
        money = money
    )

    if new_bill:
        status = "SUCCESS"
    else:
        status = "FAILURE"

    return HttpResponse(json.dumps({'status': status}))
