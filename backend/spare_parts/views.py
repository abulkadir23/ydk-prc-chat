from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import SparePart
from .serializers import SparePartSerializer

class SparePartViewSet(viewsets.ModelViewSet):
    queryset = SparePart.objects.all()
    serializer_class = SparePartSerializer
    permission_classes = [IsAuthenticated] 