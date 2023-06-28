from rest_framework import serializers
from django.contrib.auth.models import User


class TechniqueModelSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()


class EngineModelSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()


class TransmissionModelSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()


class DriveAxleModelSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()


class SteerableAxleModelSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'groups', 'username']


class ClientSerializer(serializers.Serializer):
    user = UserSerializer()
    name = serializers.CharField()
    description = serializers.CharField()


class ServiceCompanySerializer(serializers.Serializer):
    user = UserSerializer()
    name = serializers.CharField()
    description = serializers.CharField()


class CarSerializer(serializers.Serializer):
    serial_number = serializers.CharField()
    technique_model = TechniqueModelSerializer()
    engine_model = EngineModelSerializer()
    engine_number = serializers.CharField()
    transmission_model = TransmissionModelSerializer()
    transmission_number = serializers.CharField()
    drive_axle_model = DriveAxleModelSerializer()
    drive_axle_number = serializers.CharField()
    steerable_axle_model = SteerableAxleModelSerializer()
    steerable_axle_number = serializers.CharField()
    supply_contract = serializers.CharField()
    shipping_date = serializers.DateField()
    consignee = serializers.CharField()
    delivery_address = serializers.CharField()
    equipment = serializers.CharField()
    client = ClientSerializer()
    service_company = ServiceCompanySerializer()


class MiniCarSerializer(serializers.Serializer):
    serial_number = serializers.CharField()
    technique_model = TechniqueModelSerializer()
    engine_model = EngineModelSerializer()
    engine_number = serializers.CharField()
    transmission_model = TransmissionModelSerializer()
    transmission_number = serializers.CharField()
    drive_axle_model = DriveAxleModelSerializer()
    drive_axle_number = serializers.CharField()
    steerable_axle_model = SteerableAxleModelSerializer()
    steerable_axle_number = serializers.CharField()


class TypeMaintenanceSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()


class OrganizationMaintenanceSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()


class MaintenanceSerializer(serializers.Serializer):
    type_maintenance = OrganizationMaintenanceSerializer()
    maintenance_date = serializers.DateField()
    operating_time = serializers.IntegerField()
    order = serializers.CharField()
    order_date = serializers.DateField()
    organization_maintenance = OrganizationMaintenanceSerializer()
    car = CarSerializer()
    service_company = ServiceCompanySerializer()


class FailureNodeSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()


class RecoveryMethodSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()


class ComplaintsSerializer(serializers.Serializer):
    date_of_refusal = serializers.DateField()
    operating_time = serializers.IntegerField()
    failure_node = FailureNodeSerializer
    description_failure = serializers.CharField()
    recovery_method = RecoveryMethodSerializer()
    parts_used = serializers.CharField()
    date_of_restoration = serializers.DateField()
    equipment_downtime = serializers.IntegerField()
    car = CarSerializer()
    service_company = ServiceCompanySerializer()
