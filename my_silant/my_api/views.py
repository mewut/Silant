
from backend.models import Car, Maintenance, Complaints
from rest_framework import viewsets, generics
from .serializers import CarSerializer, MaintenanceSerializer, ComplaintsSerializer, MiniCarSerializer
from rest_framework.permissions import IsAuthenticated
from .serializers import ComplaintsSerializer


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all().order_by('shipping_date')
    serializer_class = CarSerializer
    def get_serializer_class(self):
        if not self.request.user.is_authenticated:
            return MiniCarSerializer 
        else:
            return CarSerializer 
        

class MaintenanceList(generics.ListAPIView):
    serializer_class = MaintenanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.has_perm('silant.view_maintenance_noclient') == False:
            queryset = Maintenance.objects.filter(car__client__user=user)
        elif user.has_perm('silant.view_maintenance_noservice') == False:
            queryset = Maintenance.objects.filter(service_company__user=user)
        elif user.has_perm('silant.add_car') == True:
            queryset = Maintenance.objects.all()
        else:
            queryset = Maintenance.objects.none()
        return queryset
    
    
class ComplaintsList(generics.ListAPIView):
    serializer_class = ComplaintsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.has_perm('silant.view_complaints_noclient') == False:
            queryset = Complaints.objects.filter(car__client__user=user)
        elif user.has_perm('silant.view_complaints_noservice') == False:
            queryset = Complaints.objects.filter(service_company__user=user)
        elif user.has_perm('silant.add_car') == True:
            queryset = Complaints.objects.all()
        else:
            queryset = Complaints.objects.none()
        return queryset
