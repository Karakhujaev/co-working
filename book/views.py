from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Book, Resident
from .serializers import BookedSerializer
from room.models import Room


class BookAPIView(APIView):
    """ API to book room """

    def post(self, request):
        resident_id = request.data.get('resident')
        room_id = request.data.get('room')
        check_in = request.data.get('check_in')
        check_out = request.data.get('check_out')
        
        conflicting_bookings = Book.objects.filter(
            room_id=room_id,
            check_in__lt=check_out,
            check_out__gt=check_in
        )
        
        if conflicting_bookings.exists():
            return Response(
                    {'message': 'Room is not available for the given date and time'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
        resident = Resident.objects.get(id=resident_id)
        room = Room.objects.get(id=room_id)
        booking = Book.objects.create(
            resident=resident,
            room=room,
            check_in=check_in,
            check_out=check_out
        )
        
        serializer = BookedSerializer(booking)
        return Response(serializer.data, status=status.HTTP_201_CREATED)