from django.contrib import admin
from .models import Car, Complaints, Drive_axle_model, Engine_model, Failure_node, Maintenance, Organization_maintenance, Recovery_method, Service_company, Steerable_axle_model, Technique_model, Transmission_model, Type_maintenance, Client

admin.site.register(Car)
admin.site.register(Complaints)
admin.site.register(Maintenance)
admin.site.register(Technique_model)
admin.site.register(Engine_model)
admin.site.register(Transmission_model)
admin.site.register(Drive_axle_model)
admin.site.register(Steerable_axle_model)
admin.site.register(Service_company)
admin.site.register(Type_maintenance)
admin.site.register(Organization_maintenance)
admin.site.register(Failure_node)
admin.site.register(Recovery_method)
admin.site.register(Client)

# проверь, ничего ли не забыла