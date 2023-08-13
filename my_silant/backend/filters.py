from django_filters import FilterSet  
from .models import Car, Maintenance, Complaints, ServiceCompany, TechniqueModel, EngineModel, TransmissionModel, DriveAxleModel, SteerableAxleModel, TypeMaintenance, FailureNode, RecoveryMethod


class CarFilter(FilterSet):
    class Meta:
        model = Car
        fields = (
           'technique_model',
           'engine_model',
           'transmission_model',
           'steerable_axle_model',
           'drive_axle_model',
        )  


class MaintenanceFilter(FilterSet):
    class Meta:
        model = Maintenance
        fields = (
            'type_maintenance',
            'serial_number',
            'service_company',
        )


class ComplaintsFilter(FilterSet):
    class Meta:
        model = Complaints
        fields =(
            'failure_node',
            'recovery_method',
            'service_company',
        )

# для списков
class ServiceCompanyFilter(FilterSet):
    class Meta:
        model = ServiceCompany
        fields = (
            'name',
            'description',
        )


class TechniqueModelFilter(FilterSet):
    class Meta:
        model = TechniqueModel
        fields = (
            'name',
            'description',
        )


class EngineModelFilter(FilterSet):
    class Meta:
        model = EngineModel
        fields = (
            'name',
            'description',
        )


class TransmissionModelFilter(FilterSet):
    class Meta:
        model = TransmissionModel
        fields = (
            'name',
            'description',
        )

class DriveAxleModelFilter(FilterSet):
    class Meta:
        model = DriveAxleModel
        fields = (
            'name',
            'description',
        )


class SteerableAxleModelFilter(FilterSet):
    class Meta:
        model = SteerableAxleModel
        fields = (
            'name',
            'description',
        )


class TypeMaintenanceFilter(FilterSet):
    class Meta:
        model = TypeMaintenance
        fields = (
            'name',
            'description',
        )


class FailureNodeFilter(FilterSet):
    class Meta:
        model = FailureNode
        fields = (
            'name',
            'description',
        )


class RecoveryMethodFilter(FilterSet):
    class Meta:
        model = RecoveryMethod
        fields = (
            'name',
            'description',
        )
