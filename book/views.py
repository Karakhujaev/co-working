from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Book, Resident
from .serializers import BookedSerializer, ResidentSerializer
from room.models import Room
from rest_framework.generics import GenericAPIView


class BookAPIView(APIView):
    """ API to book room """

    def post(self, request, pk):
        resident = request.data.get('resident')["name"]
        start = request.data.get('start')
        end = request.data.get('end')
        
        conflicting_bookings = Book.objects.filter(
            room=pk,
            start__lt=start,
            end__gt=end
        )
        
        if conflicting_bookings.exists():
            return Response(
                    {'message': 'Room is not available for the given date and time'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
        resident = Resident.objects.get(name=resident)
        room = Room.objects.get(id=pk)
        booking = Book.objects.create(
            resident=resident,
            room=room,
            start=start,
            end=end
        )
        
        serializer = BookedSerializer(booking)
        response_data = {
                "success": True,
                "message": "Room has booked successfully",
                "result": serializer.data
            }
        return Response(response_data, status=status.HTTP_201_CREATED)


class ResidentAPIView(GenericAPIView):
    queryset = Resident.objects.all()
    serializer_class = ResidentSerializer

    def post(self, request):
        serilazier = self.get_serializer(data=request.data)

        if serilazier.is_valid():
            serilazier.save()
            return Response(serilazier.data, status=status.HTTP_201_CREATED)
        return Response(serilazier.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk=None):
        residents = self.get_queryset()
        serializer = self.get_serializer(residents, many=True)

        if not serializer.data:
            return Response({"success": False, "message": "Resident not found"}, status=status.HTTP_404_NOT_FOUND)   

        return Response({"success": True, "results":serializer.data}, status=status.HTTP_200_OK)   

