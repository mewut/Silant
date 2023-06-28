from django.urls import include, path
from rest_framework import routers
from .views import *

router = routers.DefaultRouter()
router.register(r'cars', CarViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('complaints/', ComplaintsList.as_view(), name='complaints-list'),
    path('maintenances/', MaintenanceList.as_view(), name='maintenances-list'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
