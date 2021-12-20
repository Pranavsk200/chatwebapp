import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import *
from django.contrib.auth import get_user_model
from .serilizer import RoomSerializers
import datetime
from django.http import HttpResponseNotFound
from django.contrib.auth.models import User
from .views import is_online

User=get_user_model()
class ChatConsumer(WebsocketConsumer):
    def fetch_messages(self,data):
        usernam = self.scope['user'].username
        boo = False

        user = Users.objects.filter(id=data['userId']).update(online=True)

        room= Room.objects.filter(id=data['roomId'])[0]
        for rooms in room.friends.all():
            if rooms.user != self.scope['user']:
                friend = rooms
                break
        for message in room.friends.all():
            if message.user == self.scope['user']:
                boo = True
                break
        if friend.online == True:
            online = 'online'
        else:
            online = 'last seen '+str(friend.lastSeen.time().hour)+':'+str(friend.lastSeen.time().minute)
        if boo==True:
            context={
                'commnad':'rooms_messages',
                'messages':self.messages_to_json(room),
                'friends': self.friendsNames_to_json(room),
                'online': online
            }
            return self.send_room_chat_messages(context)
        else:
            return HttpResponseNotFound('<p>you are not allowed in this room<p>')


    def serilizeRoom(self,rooms):
        result=[]
        for room in rooms:
            result.append(self.rooms_to_json(room))
        return result

    def new_message(self,data):
        roomId=data['roomId']
        user = User.objects.filter(username=self.scope['user'])[0]
        RRoom=Room.objects.filter(id=roomId)[0]
        createMessage=messages(
            user=user,
            massage=data['message']
        )
        createMessage.save()
        RRoom.roomMessages.add(createMessage)
        Room.objects.filter(id=roomId).update(lastMessage=createMessage)

        context={
            'command':'new_message',
            'message': self.message_to_json(createMessage)
        }
        return self.send_chat_messages(context)

    command={
        'fetch_messasges': fetch_messages,
        'new_messages':new_message,
    }


    def friendsNames_to_json(self,room):
        result=[]
        for name in room.friends.all():
            result.append(self.friendsName_to_json(name))
        return result

    def friendsName_to_json(self,name):
        return{
            'userName': name.user.username
        }

    def messages_to_json(self,room):
        result=[]
        for message in room.roomMessages.all():
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self,messages):
        return{
            'user':messages.user.username,
            'content':messages.massage,
            'time':str(messages.data.time().hour)+":"+str(messages.data.time().minute),
            'date':str(messages.data.date().day)+"/"+str(messages.data.date().month)+"/"+str(messages.data.date().year),
            'sent':str(messages.sent)
        }


    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        usern = Users.objects.filter(user=self.scope['user']).update(online=False)
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        data = json.loads(text_data)
        self.command[data['command']](self,data)

    def send_chat_messages(self,data):
        message = data
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_room_chat_messages(self,data):
        async_to_sync(self.send(text_data=json.dumps(data)))

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        async_to_sync(self.send(text_data=json.dumps(message)))
