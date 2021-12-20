from rest_framework import serializers
from .models import *


class FriendsSerializer(serializers.ModelSerializer):
    class Meta:
        model = messages
        field = '__all__'


class RoomSerializers(serializers.ModelSerializer):
    messages = FriendsSerializer(read_only=True, many=True)
    class Meta:
        model= Room
        fields = ['id','messages','friends']
        depth = 1