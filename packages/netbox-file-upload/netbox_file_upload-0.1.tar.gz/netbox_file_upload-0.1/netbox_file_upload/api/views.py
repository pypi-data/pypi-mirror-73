from rest_framework.viewsets import ModelViewSet

from .serializers import DeviceSerializer
from dcim.models import Device

class DeviceViewSet(ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer