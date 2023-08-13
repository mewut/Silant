from rest_framework import serializers
from .models import *


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ('__all__')


class MaintenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maintenance
        fields = ('__all__')
        

class ComplaintsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaints
        fields = ('__all__')
