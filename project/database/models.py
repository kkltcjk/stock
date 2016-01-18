#-*- coding:UTF-8 -*-
from django.db import models

# Create your models here.

class bill(models.Model):
    name = models.CharField(max_length=50)
    money = models.IntegerField(default=0)
