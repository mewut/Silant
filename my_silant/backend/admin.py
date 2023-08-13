from django.contrib import admin
from .models import *

admin.site.register(Car)
admin.site.register(Complaints)
admin.site.register(Maintenance)
admin.site.register(TechniqueModel)
admin.site.register(EngineModel)
admin.site.register(TransmissionModel)
admin.site.register(DriveAxleModel)
admin.site.register(SteerableAxleModel)
admin.site.register(ServiceCompany)
admin.site.register(TypeMaintenance)
admin.site.register(OrganizationMaintenance)
admin.site.register(FailureNode)
admin.site.register(RecoveryMethod)
