from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.validators import ValidationError

from datetime import datetime, time
from django.utils import timezone
from django.utils.timezone import make_aware

from room.models import Room
from .models import Book, Resident
from .serializers import BookSerializer, ResidentSerializer


class BookAPIView(APIView):
    """ API to book a room """

    def post(self, request, pk):
        resident_name = request.data.get('resident', {}).get('name')
        start = request.data.get('start')
        end = request.data.get('end')
        
        if not resident_name or not start or not end:
            return Response(
                {'message': "Buyurtmachi ismi, boshlanish va tugash vaqti kerak."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            start_time = timezone.make_aware(datetime.strptime(start, '%d-%m-%Y %H:%M'))
            end_time = timezone.make_aware(datetime.strptime(end, '%d-%m-%Y %H:%M'))

        except ValueError:
            raise ValidationError("Vaqt formati noto‘g‘ri. KK-OO-YYYY SS:DD formatidan foydalaning.")
        
        if start_time >= end_time:
            raise ValidationError("Boshlanish vaqti tugash vaqtidan oldin bo'lishi kerak.")
        
        if start_time < timezone.now():
            raise ValidationError("Buyurtma vaqti o'tmishda bo'lishi mumkin emas.")
        
        working_start_time = timezone.make_aware(datetime.combine(start_time.date(), time(8, 0)))
        working_end_time = timezone.make_aware(datetime.combine(start_time.date(), time(20, 0)))
        
        if start_time < working_start_time or end_time > working_end_time:
            raise ValidationError("Coworking ish vaqti (08:00 dan 20:00 gacha)")
        
        conflicting_bookings = Book.objects.filter(
            room=pk,
            start__lte=end_time,
            end__gte=start_time
        )
        
        if conflicting_bookings.exists():
            return Response(
                {'message': 'Belgilangan sana va vaqt uchun xona mavjud emas'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        resident = Resident.objects.get(name=resident_name)
        room = Room.objects.get(id=pk)
        booking = Book.objects.create(
            resident=resident,
            room=room,
            start=start_time,
            end=end_time
        )
        
        # serializer = BookSerializer(booking)
        response_data = {
            "success": True,
            "message": "Xona muvaffaqiyatli qo'shildi",
            "result": {
                "id": booking.id,
                "resident": {
                    "name": resident_name
                },
                "room": room.id,
                "start": start_time.strftime('%d-%m-%Y %H:%M'),
                "end": end_time.strftime('%d-%m-%Y %H:%M')
            }
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
            return Response({"success": False, "message": "topilmadi"}, status=status.HTTP_404_NOT_FOUND)   

        return Response({"success": True, "results":serializer.data}, status=status.HTTP_200_OK)   
    

class AvailabilityAPIView(APIView):
    """ API to get available times for a room on a given date """

    def get(self, request, pk):
        date_param = request.query_params.get('date', None)

        if date_param:
            try:
                date = datetime.strptime(date_param, '%d-%m-%Y').date()
                
            except ValueError:
                date = datetime.now().date()
        else:
            date = datetime.now().date()

        if date < datetime.now().date():
            return Response({"error": "O'tgan sanalar mavjud emas"}, status=status.HTTP_400_BAD_REQUEST)

        start_time = make_aware(datetime.combine(date, datetime.min.time()).replace(hour=8, minute=0))
        end_time = make_aware(datetime.combine(date, datetime.min.time()).replace(hour=20, minute=0))

        bookings = Book.objects.filter(room=pk, start__date=date).order_by('start')

        if not bookings.exists():
            available_times = [{
                "start": start_time.strftime('%d-%m-%Y %H:%M'),
                "end": end_time.strftime('%d-%m-%Y %H:%M')
            }]
        else:
            available_times = []
            last_end_time = start_time

            for booking in bookings:
                if booking.start > last_end_time:
                    available_times.append({
                        "start": last_end_time.strftime('%d-%m-%Y %H:%M'),
                        "end": booking.start.strftime('%d-%m-%Y %H:%M')
                    })

                last_end_time = booking.end

            if last_end_time < end_time:
                available_times.append({
                    "start": last_end_time.strftime('%d-%m-%Y %H:%M'),
                    "end": end_time.strftime('%d-%m-%Y %H:%M')
                })

        return Response(available_times)