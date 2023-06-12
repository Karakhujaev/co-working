from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, GenericAPIView, RetrieveAPIView
from django.core.exceptions import ObjectDoesNotExist

from .models import Room
from .serializers import RoomSerializer

class RoomCreateAPIView(GenericAPIView):
    """ API to create room """

    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                        {
                            "success":True, 
                            "message": "Room has been created successfully!",
                            "result": serializer.data
                        },
                        status=status.HTTP_201_CREATED
                    )   

        return Response(
                    {
                        "success":False, 
                        "error": "Error in creating room!"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )


class RoomDetailAPIView(RetrieveAPIView):
    """ API to get rooms by id """

    queryset = Room
    serializer_class = RoomSerializer

    def retrieve(self, request, pk):
        try:
            room = self.get_object()
            serializer = self.get_serializer(room)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ObjectDoesNotExist:

            return Response(
                {
                    "success": False,
                    "error": "NOT FOUND"
                },
                status=status.HTTP_404_NOT_FOUND
            )


class RoomAPIView(ListAPIView):
    """ API to search rooms by name, filter by type """

    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['type']

    class Pagination(PageNumberPagination):
        page_size_query_param = 'page_size'
        max_page_size = 10

    pagination_class = Pagination

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        response_data = {
            'page': self.request.query_params.get('page', 1),
            'count': len(queryset),
            'page_size': int(self.request.query_params.get('page_size', self.pagination_class.page_size or 10)),
            'results': serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def get_queryset(self):
        queryset = super().get_queryset()

        name_query = self.request.query_params.get('search', None)
        if name_query:
            queryset = queryset.filter(name__icontains=name_query)

        room_type = self.request.query_params.get('type', None)
        if room_type:
            queryset = queryset.filter(type=room_type)

        return queryset