from __future__ import unicode_literals
from django.db import models

class User(models.Model):
    name = models.CharField(max_length = 100)
    username = models.CharField(max_length = 100)
    email = models.CharField(max_length = 100)
    password = models.CharField(max_length = 100)
    created_at = models.DateTimeField(auto_now_add = True)

class Trip(models.Model):
    by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="planner")
    wishers = models.ManyToManyField(User, related_name="desirer") #this is a list
    destination = models.CharField(max_length = 100)
    start = models.CharField(max_length = 100)
    end = models.CharField(max_length = 100)
    plan = models.CharField(max_length = 100)
    created_at = models.DateTimeField(auto_now_add = True)
