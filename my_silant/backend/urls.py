from django.urls import path, include
from .views import CarCreateView, CarDetailView, CarUpdateView, CarListView, ComplaintsCreateView, ComplaintsUpdateView, ComplaintsListView, MaintenanceCreateView, MaintenanceUpdateView, MaintenanceListView, car_directory, maintenance_directory, complaint_directory, login
from django.contrib.auth import views as auth_views


urlpatterns = [

    path('', CarListView.as_view()),
    path('<int:pk>/', CarDetailView.as_view(), name='car_info'),
    path('create/', CarCreateView.as_view(), name='car_create'),
    path('edit/<int:pk>/', CarUpdateView.as_view(), name='edit_car'),

    path('dictionary/<str:type>/<int:id>/', car_directory),
    path('maintenances/dictionary/<str:type>/<int:id>/', maintenance_directory),
    # path('dictionary/save/', save_dictionary, name='save_dictionary'),
    # path('complaints/update/<int:pk>/', ComplaintsUpdateView.as_view(), name='complaints_update'),

    path('maintenances/', MaintenanceListView.as_view()), 
    path('maintenances/create/', MaintenanceCreateView.as_view(), name='create_maintenance'),
    path('maintenances/edit/<int:pk>/', MaintenanceUpdateView.as_view(), name='edit_maintenance'),

    path('complaints/', ComplaintsListView.as_view()), 
    path('complaints/create/', ComplaintsCreateView.as_view(), name='create_complaints'),
    path('complaints/edit/<int:pk>/', ComplaintsUpdateView.as_view(), name='edit_complaints'), 

   # path('complaints/dictionary/<str:type>/<int:id>/', complaint_directory, name='complaint_directory'),

    path('accounts/', include('allauth.urls')),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]
