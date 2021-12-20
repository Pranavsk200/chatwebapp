from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as dj_login,logout
from .models import *
from django.utils.safestring import mark_safe
from django.http import JsonResponse
from rest_framework import generics,viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
import json

# Create your views here.
# def chartroom(request):
#     if request.user.is_authenticated:
#         rooms=Room.objects.all()
#         context={
#             'rooms':rooms
#         }
#         return render(request,"index.html",context)
#     else:
#         return redirect("login")    

def home(request):
    if request.user.is_authenticated:    
        user = Users.objects.filter(user=request.user)[0]
        rooms=Room.objects.filter(friends=user)
        context={
            'rooms':rooms,
        }
        return render(request,'homee.html', context)
    else:
        return redirect("login")    
    
        

def login(request):
    if request.method=='POST':
        name = request.POST['username']
        password = request.POST['pass']
        user=authenticate(username=name, password=password)
        if user is not None:
            dj_login(request, user)
            current_user=request.user
            return redirect("chatroom")
        else:
            messages.info(request, "username or password is incorrect") 
            return redirect("login")   
    else:    
        return render(request,"login.html")
     

def signin(request):
    if request.method == 'POST' :
        username = request.POST['username']
        first_name = request.POST['first_name']
        number = request.POST['number']
        email = request.POST['email']
        password = request.POST['pass']
        repassword = request.POST['repass']
        if password==repassword:
            if User.objects.filter(email=email).exists():
                messages.info(request,"Email already exist")
                return redirect("signin")
            elif User.objects.filter(username=username).exists():
                messages.info(request,"user name already exists,please resistor with another username") 
                return redirect("signin")   
            else:    
                user =User.objects.create_user(username=username,first_name=first_name, email=email, password=password)
                user.save()
                print('user created')
                return redirect("login")
        else:
            messages.info(request, "conform passowerd and password are not matching")
    else:
        return render(request, "sign-in.html")              
            
def room(request,roomid):
    if request.user.is_authenticated:
        user = Users.objects.filter(user=request.user)[0]
        rooms=Room.objects.filter(friends=user)
        context={
            'rooms':rooms,
            'roomid':mark_safe(json.dumps(roomid)),
            'userName':mark_safe(json.dumps(request.user.username)),
            'userId':mark_safe(json.dumps(user.id))  
        }
        return render(request, "index.html",context)  
    else:
        return redirect("login")      

def is_online(user):
    cUser=Users.objects.filter(user=user).update(online=True)
    cUser.online=True
    cUser.save()

def attrubuteJson(user):
    return{
        "username":str(user.username),
        "name":str(user.first_name)+" "+ str(user.last_name),
    }

def search(request, name):
    Users = User.objects.filter(username__icontains=name)
    print(Users)
    context={"data":toJson(Users)}
    return JsonResponse(context)
    
        
def toJson(users):
    data=[]
    if len(users)>1:
        for user in users.all():
            data.append(attrubuteJson(user))
    if len(users)<2:
        data = attrubuteJson(users)            
    return data    

