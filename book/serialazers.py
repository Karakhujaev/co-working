from rest_framework import serializers
from room.serializers import RoomSerializer
from .models import Resident, Booked, Room


class ResidentSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Resident
        fields = ['id', 'name']


class BookedSerializer(serializers.ModelSerializer):
    resident = serializers.PrimaryKeyRelatedField(queryset=Resident.objects.all())
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())

    class Meta:
        model = Booked
        fields = ['id', 'resident', 'room', 'check_in', 'check_out']



class BookedDetailSerializer(serializers.ModelSerializer):
    resident = ResidentSerailizer(read_only=True)
    room = RoomSerializer(read_only=True)

    class Meta:
        model = Booked
        fields = ['id', 'resident', 'room', 'check_in', 'check_out', 'created_at']

