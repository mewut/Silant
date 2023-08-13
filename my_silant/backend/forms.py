from django.forms import ModelForm
from .models import *


class MaintenanceForm(ModelForm):
    class Meta:
        model = Maintenance
        fields = [
            'type_maintenance',
            'maintenance_date',
            'operating_time',
            'order',
            'order_date',
            'organization_maintenance',
            'car',
            'service_company',
            'serial_number',
        ]


class ComplaintsForm(ModelForm):
    class Meta:
        model = Complaints
        fields = [
            'date_of_refusal',
            'operating_time',
            'failure_node',
            'description_failure',
            'recovery_method',
            'parts_used',
            'date_of_restoration',
            'equipment_downtime',
            'car',
            'service_company',
            'serial_number',
        ]


class CarForm(ModelForm):
    class Meta:
        model = Car
        fields = [
            'serial_number',
            'technique_model',
            'engine_model',
            'engine_number',
            'transmission_model',
            'transmission_number',
            'drive_axle_model',
            'drive_axle_number',
            'steerable_axle_model',
            'steerable_axle_number',
            'supply_contract',
            'shipping_date',
            'consignee',
            'delivery_address',
            'equipment',
            'client',
            'service_company',
        ]

# Формы списков
class ServiceCompanyForm(ModelForm):
    class Meta:
        model = ServiceCompany
        fields = [
            'name',
            'description',
        ]


class TechniqueModelForm(ModelForm):
    class Meta:
        model = TechniqueModel
        fields = [
            'name',
            'description',
        ]


class EngineModelForm(ModelForm):
    class Meta:
        model = EngineModel
        fields = [
            'name',
            'description',
        ]


class TransmissionModelForm(ModelForm):
    class Meta:
        model = TransmissionModel
        fields = [
            'name',
            'description',
        ]


class DriveAxleModelForm(ModelForm):
    class Meta:
        model = DriveAxleModel
        fields = [
            'name',
            'description',
        ]


class SteerableAxleModelForm(ModelForm):
    class Meta:
        model = SteerableAxleModel
        fields = [
            'name',
            'description',
        ]


class TypeMaintenanceForm(ModelForm):
    class Meta:
        model = TypeMaintenance
        fields = [
            'name',
            'description',
        ]


class FailureNodeForm(ModelForm):
    class Meta:
        model = FailureNode
        fields = [
            'name',
            'description',
        ]


class RecoveryMethodForm(ModelForm):
    class Meta:
        model = RecoveryMethod
        fields = [
            'name',
            'description',
        ]

