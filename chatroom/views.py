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
from django.http import HttpResponse

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
        user = Users.objects.get(user=request.user)
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
        user=authenticate(request, username=name, password=password)
        if user is not None:
            dj_login(request, user)
            current_user=request.user
            return redirect("home")
        else:
            #messages.success(request, "username or password is incorrect") 
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
                use = Users(user=user,mobile_no=number)
                use.save()
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
    #user = Users.objects.get(user=request.user)
    #friends = friends.objects.filter(current_user= user)
    # boo = False
    # for i in friends:
    #     if i.user.username = user.username:
    #         boo = True
    return{
        "username":str(user.username),
        "name":str(user.first_name)+" "+ str(user.last_name),
    }

def search(request, name):
    Users = User.objects.filter(username__icontains=name)

    if Users.count() <=0:
        context={"data":"no such user found"}
        return JsonResponse(context)
    else:
        context={"data":toJson(Users)}
        return JsonResponse(context)    
    
        
def toJson(users):
    data=[]
    if len(users)>0:
        for user in users.all():
            data.append(attrubuteJson(user))           
    return data    

def searchPage(request):
    return render(request,"searchPage.html")

def profile(request):
    if request.user.is_authenticated:
        userName = request.user.username
        user = User.objects.get(username=request.user.username)
        usr = Users.objects.get(user=user)
        name = str(usr.user.first_name) +" "+str(usr.user.last_name)
        context={
            'username':userName,
            'name': name
        }
        return render(request,"profile.html", context)
    else:
        return redirect("login")  

def logoutUser(request):
    if request.user.is_authenticated: 
        logout(request)
        return redirect("login") 
    else:
        return redirect("login")    

def searchResult(request, username):
    if request.user.is_authenticated:
        user = Users.objects.get(user = request.user)
        sender = relationship.objects.filter(sender = user)
        searchUser = User.objects.get(username = username) 
        searchInfo = Users.objects.get(user = searchUser)
        reciver = relationship.objects.filter(reciver = searchInfo)
        buttonName = "follow"
        if relationship.objects.filter(sender = user).filter(reciver = searchInfo).filter(status = 'send').exists():
            buttonName = "requested"
        elif relationship.objects.filter(sender = user).filter(reciver = searchInfo).filter(status = 'accepted').exists() or relationship.objects.filter(sender = searchInfo).filter(reciver = user).filter(status = 'accepted').exists():
            buttonName = "following"  
        elif relationship.objects.filter(sender = searchInfo).filter(reciver = user).filter(status = 'send').exists():
            buttonName = "accept"
        else:
            buttonName =  "follow" 

        print(buttonName)       
        
        context = {
            'username' : searchInfo.user.username,
            'name': str(searchInfo.user.first_name)+ " " + str(searchInfo.user.last_name),
            'bio' : str(searchInfo.bio),
            'buttonName': buttonName
        }
        return render(request, "searchResultPage.html", context)

    else:
        return redirect("login")    

def follow(request,username):
    if request.user.is_authenticated:
        senderUser = User.objects.get(username = username)
        senderStore = Users.objects.get(user = senderUser)
        current_user = Users.objects.get(user= request.user)
        if relationship.objects.filter(sender = current_user).filter(reciver = senderStore).exists() == False:
            relShip = relationship(sender = current_user, reciver = senderStore, status = 'send')
            relShip.save()
            return HttpResponse(" ") 
        return HttpResponse("user already exist")    
    else:
        return redirect("login")

def accept(request,username):
    if request.user.is_authenticated:
        current_user = Users.objects.get(user = request.user)
        requested_user = User.objects.get(username = username)
        requested = Users.objects.get( user=requested_user)
        if relationship.objects.filter(sender = requested).filter(reciver = current_user).filter(status = "send").exists():
            relShip = relationship.objects.filter(sender = requested).filter(reciver = current_user).filter(status = "send")
            relShip.delete()
            rel = relationship(sender = requested, reciver = current_user, status = "accepted")
            rel.save()
            if Friends.objects.filter(current_user = current_user).filter(friends = requested).exists() == False:
                if Friends.objects.filter(current_user = current_user).exists():  
                    accepter = Friends.objects.filter(current_user = current_user)
                    accepter.friends.add(requested)
                    accepter.save()
                else:
                    accepter = Friends(current_user = current_user) 
                    accepter.save()   
                    accepter.friends.add(requested)
                    accepter.save()
                if Friends.objects.filter(current_user = requested).exists():
                    if Friends.objects.filter(current_user = requested).filter(friends = current_user).exists() == False:
                        sender = Friends.objects.filter(current_user = requested)
                        sender.friends.add(current_user)
                        sender.save()
                    else:
                        return redirect({"data":"you are already friend"})    
                else:
                    sender = Friends(current_user = requested)
                    sender.save()    
                    sender.friends.add(current_user)
                    sender.save()
                room = Room()
                room.save()
                room.friends.add(current_user,requested) 
                room.save()   
            return redirect("searchResult",username=username)
        return JsonResponse({"data":"request do not exist"})    
    else:
        return redirect("login")    

def decline(request,username):
    if request.user.is_authenticated:
        current_user = Users.objects.get(user = request.user)
        requested_user = User.objects.get(username = username)
        requested = Users.objects.get( user=requested_user)
        if relationship.objects.filter(sender = requested).filter(reciver = current_user).filter(status = "send").exists():
            rel = relationship.objects.filter(sender = requested).filter(reciver = current_user).filter(status = "send")
            rel.delete()
            return redirect("searchResult",username=username)
        return HttpResponse("request do not exist")    
    else:
        return redirect("login")      
