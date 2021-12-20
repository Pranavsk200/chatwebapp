from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


# Create your models here.
class Users(models.Model):
    user=models.OneToOneField(User, on_delete=models.SET_NULL,null=True)
    mobile_no=models.IntegerField()
    lastSeen=models.DateTimeField(auto_now=True,blank=True,null=True)
    online=models.BooleanField(default=False)

    def onlineSave(self):
        self.online = True

    def __str__(self):
        return self.user.username

class messages(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE) 
    massage=models.TextField()
    data=models.DateTimeField(auto_now_add=True)    
    sent=models.BooleanField(default=False)

    def __str__(self):
        return self.massage+"---->"+self.user.username

class Room(models.Model):
    roomMessages=models.ManyToManyField(messages)
    friends=models.ManyToManyField(Users)
    lastMessage=models.ForeignKey(messages, on_delete=models.CASCADE, related_name='last_message',null=True,blank=True)


