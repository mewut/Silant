from rest_framework import generics
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import AbstractUser
from .serializers import *
from .forms import *
from .models import *
from .filters import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
 

class MaintenanceListVew(LoginRequiredMixin, ListView):
    model = Maintenance
    template_name = 'maintenance.html'

    def get_context_data(self, **kwargs):
        filter = MaintenanceFilter(self.request.GET, queryset=self.get_queryset())
        manager = self.request.user.groups.filter(name='Менеджер')
        if not manager.exists():
            is_manager = 'Нe Менеджер'
        else:
            is_manager = 'Менеджер'
        context = {'filter': filter, 'is_manager': is_manager}
        return context


class ComplaintsListVew(LoginRequiredMixin, ListView):
    model = Complaints
    context_object_name = 'complaints'
    template_name = 'complaints.html'

    def get_context_data(self, **kwargs):
        filter = ComplaintsFilter(self.request.GET, queryset=self.get_queryset()) 
        manager = self.request.user.groups.filter(name='Менеджер')
        if not manager.exists():
            is_manager = 'Нe Менеджер'
        else:
            is_manager = 'Менеджер'
        context = {'filter': filter, 'is_manager': is_manager}
        return context

# для создания
class MaintenanceCreateVew(PermissionRequiredMixin, CreateView):
    permission_required = (
        'service.add_maintenance',
    )
    template_name = 'create_maintenance.html'
    form_class = MaintenanceForm


class ComplaintsCreateVew(PermissionRequiredMixin, CreateView):
    permission_required = (
        'service.add_complaints',
    )
    template_name = 'create_complaints.html'
    form_class = ComplaintsForm


class CarCreateVew(PermissionRequiredMixin, CreateView):
    permission_required = (
        'service.add_car',
    )
    template_name = 'car_create.html'
    form_class = CarForm

# для изменения
class MaintenanceUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('service.change_maintenance',)
    template_name = 'create_maintenance.html'
    form_class = MaintenanceForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Maintenance.objects.get(pk=id)


class ComplaintsUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('service.change_complaints',)
    template_name = 'create_complaint.html'
    form_class = ComplaintsForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Complaints.objects.get(pk=id)


class CarUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('service.car_detail',)
    template_name = 'car_create.html'
    form_class = CarForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Car.objects.get(pk=id)

# для удаления 
class CarDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('service.car_delete',)
    template_name = 'car_delete.html'
    queryset = Car.objects.all()
    success_url = '/user/'           # или сделать '/'
    

class MaintenanceDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('service.delete_maintenance',)
    template_name = 'delete_maintenance.html'
    queryset = Maintenance.objects.all()
    success_url = '/maintenance/'

class ComplaintsDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('service.delete_complaints',)
    template_name = 'delete_complaints.html'
    queryset = Complaints.objects.all()
    success_url = '/complaints/'

# ищем по технике
class CarSearch(ListView):
    model = Car
    template_name = 'search.html'
    context_object_name = 'car'
    
    # будем хранить результаты поиска в списке cars. 
    # если поиск ничего не нашел, то список будет пустым. 
    def get_queryset(self, **kwargs):
        search_query = self.request.GET.get('search', '')
        if search_query:
            cars = Car.objects.filter(number_car__icontains=search_query)
        else:
            cars = []
    
        return cars
    
    # этим методом проверяем, были ли переданы результаты поиска, если нет, то добавляется соответствующее сообщение
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get('search', '')
        
        if search_query and not context['car']:
            context['car'] = 'Ничего не найдено'
        
        return context

    # проверка на авторизацию
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_aut'] = self.request.user.groups.exists()
        return context


# функция фильтрации по авторизованному пользователю
def by_user_car(request):
    is_aut = request.user.groups.exists()  
    manager = request.user.groups.filter(name='Менеджер')
    if not manager.exists():
        is_manager = 'Не Менеджер' 
    else:
        is_manager = 'Менеджер'

    filter = CarFilter(request.GET)
    if is_aut:
        if is_manager == 'Менеджер':
            car = 0
        else:
            car = Car.objects.filter(client=request.user.first_name)
            if not car.exists():
                servicelist = ServiceCompany.objects.filter(name=request.user.first_name)
                if servicelist.exists():
                    service = ServiceCompany.objects.get(name=request.user.first_name)
                    car = Car.objects.filter(service_company=service.id)
                else:
                    car = 'Техника отсутствует в базе'  
        context = {'car': car,
                   'is_aut': is_aut,
                   'filter': filter,
                   'is_manager': is_manager
                  }
    else:
        car = 'Требуется авторизация'
        context = {'car': car}
    return render(request, 'user.html', context)

def maintenance_detail(request, maintenance_id):
    is_aut = request.user.is_authenticated
    manager = request.user.groups.filter(name='Менеджер')
    if not manager.exists():
        is_manager = 'Не Менеджер'
    else:
        is_manager = 'Менеджер'
    if is_aut:
        maintenance_detail = Maintenance.objects.get(pk=maintenance_id)
        car = Car.objects.get(number_car=maintenance_detail.serial_number)
        type_maintenance = TypeMaintenance.objects.get(name=maintenance_detail.type_maintenance)
        service_company = ServiceCompany.objects.get(name=maintenance_detail.service_company)
        context = {'maintenance_detail': maintenance_detail,
                   'car': car,
                   'is_aut': is_aut,
                   'type_maintenance': type_maintenance,
                   'service_company': service_company,
                   'is_manager': is_manager
                   }
    else:
        maintenance_detail = 'Авторизуйтесь'
        context = {'maintenance_detail': maintenance_detail}
    return render(request, 'maintenance_detail.html', context)

def complaint_detail(request, complaint_id):
    is_aut = request.user.is_authenticated
    manager = request.user.groups.filter(name='Менеджер')
    if not manager.exists():
        is_manager = 'Не Менеджер'
    else:
        is_manager = 'Менеджер'
    if is_aut:
        complaint_detail = Complaints.objects.get(pk=complaint_id)
        car = Car.objects.get(number_car=complaint_detail.serial_number)
        node = FailureNode.objects.get(name=complaint_detail.failure_node)
        recovery = RecoveryMethod.objects.get(name=complaint_detail.recovery_method)
        service_company = ServiceCompany.objects.get(name=complaint_detail.service_company)
        context = {'complaint_detail': complaint_detail,
                   'car': car,
                   'is_aut': is_aut,
                   'node': node,
                   'recovery': recovery,
                   'service_company': service_company,
                   'is_manager': is_manager
                   }
    else:
        complaint_detail = 'Авторизуйтесь'
        context = {'complaint_detail': complaint_detail}
    return render(request, 'complaint_detail.html', context)

def complaint_list_car(request, car_id): 
    is_aut = request.user.is_authenticated
    manager = request.user.groups.filter(name='Менеджер')
    if not manager.exists():
        is_manager = 'Не Менеджер'
    else:
        is_manager = 'Менеджер'
    if is_aut:
        complaint_list = Complaints.objects.filter(serial_number=car_id)
        car = Car.objects.get(pk=car_id)
        context = {'complaint_list': complaint_list,
                   'car': car,
                   'is_aut': is_aut,
                   'is_manager': is_manager
                   }
    else:
        complaint_list = 'Авторизуйтесь'
        context = {'complaint_list': complaint_list}
    return render(request, 'complaint_list_car.html', context)

def maintenance_list_car(request, car_id):
    is_aut = request.user.is_authenticated
    manager = request.user.groups.filter(name='Менеджер')
    if not manager.exists():
        is_manager = 'Не Менеджер'
    else:
        is_manager = 'Менеджер'
    if is_aut:
        to_list = Maintenance.objects.filter(car_to=car_id)
        car = Car.objects.get(pk=car_id)                            
        context = {'to_list': to_list,
                   'car': car,
                   'is_aut': is_aut,
                   'is_manager': is_manager
                   }
    else:
        to_list = 'Авторизуйтесь'
        context = {'to_list': to_list}
    return render(request, 'to_list_car.html', context)

def car_detail(request, car_id):
    is_aut = request.user.is_authenticated
    manager = request.user.groups.filter(name='Менеджер')
    if not manager.exists():
        is_manager = 'Не Менеджер'
    else:
        is_manager = 'Менеджер'
    if is_aut:
        car = Car.objects.get(pk=car_id)
        technique = TechniqueModel.objects.get(name=car.technique_model)
        engine = EngineModel.objects.get(name=car.engine_model)
        trans = TransmissionModel.objects.get(name=car.transmission_model)
        axle = DriveAxleModel.objects.get(name=car.drive_axle_model)
        steerable = SteerableAxleModel.objects.get(name=car.steerable_axle_model)
        service = ServiceCompany.objects.get(name=car.service_company)
        context = {'car': car,
                   'technique': technique,
                   'is_aut': is_aut,
                   'engine': engine,
                   'trans': trans,
                   'axle': axle,
                   'steerable': steerable,
                   'service': service,
                   'is_manager': is_manager
                   }
    else:
        car = 'Авторизуйтесь'
        context = {'car': car}
    return render(request, 'car_detail.html', context)

# получение списков
class ServiceCompanyListView(PermissionRequiredMixin, ListView):
    permission_required = ('service.view_servicecompany')
    model = ServiceCompany
    context_object_name = 'servicecompany'
    template_name = 'lists/servicecompany_list.html'
    queryset = ServiceCompany.objects.all()
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = ServiceCompanyFilter(self.request.GET, queryset=self.get_queryset())  
        return context


class TechniqueModelListView(PermissionRequiredMixin, ListView):
    permission_required = ('service.view_techniquemodel')
    model = TechniqueModel
    context_object_name = 'techniquemodel'
    template_name = 'lists/techniquemodel_list.html'
    queryset = TechniqueModel.objects.all()
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = TechniqueModelFilter(self.request.GET, queryset=self.get_queryset())
        return context


class EngineModelListView(PermissionRequiredMixin, ListView):
    permission_required = ('service.view_enginemodel')
    model = EngineModel
    context_object_name = 'enginemodel'
    template_name = 'lists/enginemodel_list.html'
    queryset = EngineModel.objects.all()
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = EngineModelFilter(self.request.GET, queryset=self.get_queryset()) 
        return context


class TransmissionModelListView(PermissionRequiredMixin, ListView):
    permission_required = ('service.view_transmissionmodel')
    model = TransmissionModel
    context_object_name = 'transmissionmodel'
    template_name = 'lists/transmissionmodel_list.html'
    queryset = TransmissionModel.objects.all()
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = TransmissionModelFilter(self.request.GET, queryset=self.get_queryset())
        return context


class DriveAxleModelListView(PermissionRequiredMixin, ListView):
    permission_required = ('service.view_driveaxlemodel')
    model = DriveAxleModel
    context_object_name = 'driveaxlemodel'
    template_name = 'lists/driveaxlemodel_list.html'
    queryset = DriveAxleModel.objects.all()
    login_url = '/'

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context['filter'] = DriveAxleModelFilter(self.request.GET, queryset=self.get_queryset())  
        return context


class SteerableAxleModelListView(PermissionRequiredMixin, ListView):
    permission_required = ('service.view_steerableaxlemodel')
    model = SteerableAxleModel
    context_object_name = 'steerableaxlemodel'
    template_name = 'lists/steerableaxlemodel_list.html'
    queryset = SteerableAxleModel.objects.all()
    login_url = '/'

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context['filter'] = SteerableAxleModelFilter(self.request.GET, queryset=self.get_queryset()) 
        return context


class TypeMaintenanceListView(PermissionRequiredMixin, ListView):
    permission_required = ('service.view_typemaintenance')
    model = TypeMaintenance
    context_object_name = 'typemaintenance'
    template_name = 'lists/typemaintenance_list.html'
    queryset = TypeMaintenance.objects.all()
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = TypeMaintenanceFilter(self.request.GET, queryset=self.get_queryset())
        return context


class FailureNodeListView(PermissionRequiredMixin, ListView):
    permission_required = ('service.view_failurenode')
    model = FailureNode
    context_object_name = 'failurenode'
    template_name = 'lists/failurenode_list.html'
    queryset = FailureNode.objects.all()
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = FailureNodeFilter(self.request.GET, queryset=self.get_queryset())
        return context


class RecoveryMethodListView(PermissionRequiredMixin, ListView):
    permission_required = ('service.view_recoverymethod')
    model = RecoveryMethod
    context_object_name = 'recoverymethod'
    template_name = 'lists/recoverymethod_list.html'
    queryset = RecoveryMethod.objects.all()
    login_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = RecoveryMethodFilter(self.request.GET, queryset=self.get_queryset())
        return context

# добавление списков
class ServiceCompanyCreateVew(PermissionRequiredMixin, CreateView):
    permission_required = ('service.add_servicecompany')
    template_name = 'lists/create.html'
    form_class = ServiceCompanyForm
    login_url = '/'


class TechniqueModelCreateVew(PermissionRequiredMixin, CreateView):
    permission_required = ('service.add_techniquemodel')
    template_name = 'lists/create.html'
    form_class = TechniqueModelForm
    login_url = '/'


class EngineModelCreateVew(PermissionRequiredMixin, CreateView):
    permission_required = ('service.add_enginemodel')
    template_name = 'lists/create.html'
    form_class = EngineModelForm
    login_url = '/'


class TransmissionModelCreateVew(PermissionRequiredMixin, CreateView):
    permission_required = ('service.add_transmissionmodel')
    template_name = 'lists/create.html'
    form_class = TransmissionModelForm
    login_url = '/'


class DriveAxleModelCreateVew(PermissionRequiredMixin, CreateView):
    permission_required = ('service.add_driveaxlemodel')
    template_name = 'lists/create.html'
    form_class = DriveAxleModelForm
    login_url = '/'


class SteerableAxleModelCreateVew(PermissionRequiredMixin, CreateView):
    permission_required = ('service.add_SteerableAxleModel')
    template_name = 'lists/create.html'
    form_class = SteerableAxleModelForm
    login_url = '/'


class TypeMaintenanceCreateVew(PermissionRequiredMixin, CreateView):
    permission_required = ('service.add_TypeMaintenance')
    template_name = 'lists/create.html'
    form_class = TypeMaintenanceForm
    login_url = '/'


class FailureNodeCreateVew(PermissionRequiredMixin, CreateView):
    permission_required = ('service.add_failurenode')
    template_name = 'lists/create.html'
    form_class = FailureNodeForm
    login_url = '/'


class RecoveryMethodCreateVew(PermissionRequiredMixin, CreateView):
    permission_required = ('service.add_recoverymethod')
    template_name = 'lists/create.html'
    form_class = RecoveryMethodForm
    login_url = '/'

# удаление списков
class ServiceCompanyDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('service.delete_servicecompany')
    template_name = 'lists/delete_servicecompany.html'
    queryset = ServiceCompany.objects.all()
    success_url = '/servisecomp/'
    login_url = '/'


class TechniqueModelDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('service.delete_techniquemodel')
    template_name = 'lists/delete_techniquemodel.html'
    queryset = TechniqueModel.objects.all()
    success_url = '/modeltech/'
    login_url = '/'


class EngineModelDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('service.delete_enginemodel')
    template_name = 'lists/delete_enginemodel.html'
    queryset = EngineModel.objects.all()
    success_url = '/modeleng/'
    login_url = '/'


class TransmissionModelDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('service.delete_transmissionmodel')
    template_name = 'lists/delete_transmissionmodel.html'
    queryset = TransmissionModel.objects.all()
    success_url = '/modeltrans/'
    login_url = '/'


class DriveAxleModelDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('service.delete_driveaxlemodel')
    template_name = 'lists/delete_driveaxlemodel.html'
    queryset = DriveAxleModel.objects.all()
    success_url = '/modelaxel/'
    login_url = '/'


class SteerableAxleModelDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('service.delete_SteerableAxleModel')
    template_name = 'lists/delete_SteerableAxleModel.html'
    queryset = SteerableAxleModel.objects.all()
    success_url = '/modelsteer/'
    login_url = '/'


class TypeMaintenanceDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('service.delete_TypeMaintenance')
    template_name = 'lists/delete_TypeMaintenance.html'
    queryset = TypeMaintenance.objects.all()
    success_url = '/servisetype/'
    login_url = '/'


class FailureNodeDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('service.delete_failurenode')
    template_name = 'lists/delete_failurenode.html'
    queryset = FailureNode.objects.all()
    success_url = '/fnode/'
    login_url = '/'


class RecoveryMethodDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = ('service.delete_recoverymethod')
    template_name = 'lists/delete_recoverymethod.html'
    queryset = RecoveryMethod.objects.all()
    success_url = '/reco/'
    login_url = '/'

# Редактирование списков
class ServiceCompanyUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('service.change_servicecompany')
    template_name = 'lists/create.html'
    form_class = ServiceCompanyForm 

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return ServiceCompany.objects.get(pk=id)
    

class TechniqueModelUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('service.change_techniquemodel')
    template_name = 'lists/create.html'
    form_class = TechniqueModelForm 

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return TechniqueModel.objects.get(pk=id)
    

class EngineModelUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('service.change_enginemodel')
    template_name = 'lists/create.html'
    form_class = EngineModelForm 

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return EngineModel.objects.get(pk=id)
    

class TransmissionModelUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('service.change_transmissionmodel')
    template_name = 'lists/create.html'
    form_class = TransmissionModelForm 

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return TransmissionModel.objects.get(pk=id)
    

class DriveAxleModelUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('service.change_driveaxlemodel')
    template_name = 'lists/create.html'
    form_class = DriveAxleModelForm 

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return DriveAxleModel.objects.get(pk=id)
    

class SteerableAxleModelUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('service.change_SteerableAxleModel')
    template_name = 'lists/create.html'
    form_class = SteerableAxleModelForm 

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return SteerableAxleModel.objects.get(pk=id)
    

class TypeMaintenanceUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('service.change_TypeMaintenance')
    template_name = 'lists/create.html'
    form_class = TypeMaintenanceForm 

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return TypeMaintenance.objects.get(pk=id)
    

class FailureNodeUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('service.change_failurenode')
    template_name = 'lists/create.html'
    form_class = FailureNodeForm 

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return FailureNode.objects.get(pk=id)
    

class RecoveryMethodUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = ('service.change_recoverymethod')
    template_name = 'lists/create.html'
    form_class = RecoveryMethodForm 

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return RecoveryMethod.objects.get(pk=id)

# Вьюхи для API
class CarAPIVew(generics.ListAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class MaintenanceAPIVew(generics.ListAPIView):
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer


class ComplaintAPIVew(generics.ListAPIView):
    queryset = Complaints.objects.all()
    serializer_class = ComplaintsSerializer
