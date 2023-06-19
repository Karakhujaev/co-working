from rest_framework import serializers
from .models import Resident, Book
from room.models import Room


class ResidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resident
        fields = ['id', 'name']


class BookSerializer(serializers.ModelSerializer):
    resident = ResidentSerializer()
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())

    class Meta:
        model = Book
        fields = ['id', 'resident', 'room', 'start', 'end']




