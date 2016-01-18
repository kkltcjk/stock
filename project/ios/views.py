# coding=utf-8
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
import json

from conf import website

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


def bill(request):
    return render(request, website.bill)
