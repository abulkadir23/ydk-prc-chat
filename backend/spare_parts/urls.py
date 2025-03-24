from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SparePartViewSet

router = DefaultRouter()
router.register(r'', SparePartViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 