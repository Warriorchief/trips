
from django.shortcuts import render, redirect
from .models import User,Trip
import bcrypt
import datetime
import re
from django.contrib import messages
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

def index(request):
    # User.objects.all().delete()
    # Trip.objects.all().delete()
    return render(request, "take4/index.html")

def register(request):
    if request.method != 'POST':
        print("You have gotten to this page by invalid means!")
        return redirect('/')
    wrong = False
    name = request.POST['name'].lower()
    username = request.POST['username']
    password = request.POST['password'].encode()
    confirm_password = request.POST['confirm_password'].encode()
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    if len(name) <3 :
        wrong = True
        messages.warning(request, "Name must be at least 3 characters!")
    if len(username) <3:
        wrong = True
        messages.warning(request, "Username must be at least 3 characters!")
    if len(password) < 8:
        wrong = True
        messages.warning(request, "Password must be at least 8 characters!")
    if password != confirm_password:
        wrong = True
        messages.warning(request, "Your passwords must match!")
    if len(name)>3 and not name.isalpha():
        wrong = True
        messages.warning(request, "Name must consist of letters ONLY!")
    if wrong:
        return redirect('/')
    else:
        messages.success(request, "Registration successful! ")
        request.session['name']=name
        request.session['username'] = username
        User.objects.create(name = name, username = username, password= hashed)
        thisperson_list = User.objects.filter(username=username, name=name)
        request.session['user_id'] = thisperson_list[0].id
        return redirect('/success')

def login(request):
    username = request.POST['username']
    password = request.POST['password']
    username_list = User.objects.filter(username=username)
    if username_list:
        hashed = username_list[0].password
        if bcrypt.hashpw(password.encode(), hashed.encode()) == hashed.encode():
            request.session['user_id'] = username_list[0].id
            request.session['name'] = username_list[0].name
            return redirect('/success')
        else:
            messages.warning(request, "Password does not match username!")
            return redirect('/')
    else:
        messages.warning(request, "Username not recognized!")
        return redirect('/')

def success(request):
    me = User.objects.get(id = request.session['user_id'])
    mytrips = Trip.objects.filter(wishers=me)
    mytripsids = mytrips.values_list('id')
    othertrips = Trip.objects.exclude(id__in = mytripsids)
    context = {
        "mytrips": mytrips,
        "othertrips": othertrips,
        }
    return render (request, "take4/travels.html", context)

def additem(request):
    return render (request, "take4/travels/add.html")

def addtrip(request,trip_id):
    me = User.objects.get(id = request.session['user_id'])
    thistrip = Trip.objects.get(id=trip_id)
    thistrip.wishers.add(me)
    print "-----> just added someone to the wishers field"
    return redirect('/success')

def showitem(request,trip_id):
    me = User.objects.get(id = request.session['user_id'])
    thistrip = Trip.objects.get(id=trip_id)
    wishers = thistrip.wishers.all()
    context = {
    "thistrip": thistrip,
    "wishers": wishers,
        }
    return render (request, "take4/destination.html", context)

def createtrip(request):
    if request.method != 'POST':
        print("You have gotten to this page by invalid means!")
        return redirect('/')
    wrong = False
    destination = request.POST['destination']
    plan = request.POST['plan']
    start = request.POST['start']
    end = request.POST['end']
    wrong = False
    if len(destination) <1 or len(plan) <1:
        wrong = True
        messages.warning(request, "You can't leave any fields blank!")
    if start < datetime.date.today:
        wrong = True
        message.warning(request, "Trip must start in the future")
    if not end > start:
        wrong = True
        messages.warning(request, "End date must be after start date!")
    if wrong:
        return redirect('/additem')
    me = User.objects.get(id = request.session['user_id'])
    Trip.objects.create(by = me, destination = destination, start = start, end = end, plan = plan)
    thistrip = Trip.objects.get(plan = plan, destination=destination)
    thistrip.wishers.add(me)
    return redirect ('/success')

def logout(request):
    del request.session['user_id']
    return redirect('/')
