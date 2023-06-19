from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, GenericAPIView, RetrieveAPIView
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView


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



class RoomDetailAPIView(APIView):
    """ API to get a room by ID """

    def get(self, request, pk):
        try:
            room = Room.objects.get(id=pk)
            serializer = RoomSerializer(room)
            return Response(serializer.data)
        except Room.DoesNotExist:
            return Response({"error": "topilmadi"}, status=404)



class RoomAPIView(ListAPIView):
    """API to search rooms by name, filter by type"""

    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['type']
    pagination_class = PageNumberPagination
    page_size_query_param = 'page_size'
    max_page_size = 10

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        page_size = int(request.query_params.get('page_size', self.pagination_class.page_size))
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer(paginated_queryset, many=True)

        return Response({
            'page': paginator.page.number if paginator.page is not None else 1,
            'count': paginator.page.paginator.count if paginator.page is not None else 0,
            'page_size': page_size,
            'results': serializer.data
        })

    def get_queryset(self):
        queryset = super().get_queryset()

        name_query = self.request.query_params.get('search', None)
        if name_query:
            queryset = queryset.filter(name__icontains=name_query)

        room_type = self.request.query_params.get('type', None)
        if room_type:
            queryset = queryset.filter(type=room_type)

        return queryset