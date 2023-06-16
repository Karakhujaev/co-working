from rest_framework import serializers
from room.serializers import RoomSerializer
from .models import Resident, Book, Room

class ResidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resident
        fields = ['id', 'name']


class BookedSerializer(serializers.ModelSerializer):
    resident = ResidentSerializer()
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())

    class Meta:
        model = Book
        fields = ['id', 'resident', 'room', 'start', 'end']



class BookedDetailSerializer(serializers.ModelSerializer):
    resident = ResidentSerializer(read_only=True)
    room = RoomSerializer(read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'resident', 'room', 'check_in', 'check_out', 'created_at']


