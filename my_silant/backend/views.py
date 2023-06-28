from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import CarForm, ComplaintsForm, MaintenanceForm
from .models import *
from .filters import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
 

class CarCreateView(PermissionRequiredMixin, CreateView):
    model = Car
    form_class = CarForm
    template_name = 'car_create.html'                
    permission_required = ('silant.add_car',)
    success_url = '/cars/'                         

    def form_valid(self, form): 
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return redirect(self.get_success_url())
    

class CarUpdateView(PermissionRequiredMixin, UpdateView):
    form_class = CarForm
    model = Car
    template_name = 'car_create.html'                    
    permission_required = ('silant.change_car', )
    success_url = '/cars/'                             

    def form_valid(self, form): 
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return redirect(self.get_success_url())

def car_directory(request, id, type):
    if type == 'techniqueModel':
        namegroup = 'Модель техники'
        item = get_object_or_404(Technique_model, id=id)
    elif type == 'engineModel':
        namegroup = 'Модель двигателя'
        item = get_object_or_404(Engine_model, id=id)
    elif type == 'transmissionModel':
        namegroup = 'Модель трансмиссии'
        item = get_object_or_404(Transmission_model, id=id)
    elif type == 'driveAxleModel':
        namegroup = 'Модель ведущего моста'
        item = get_object_or_404(Drive_axle_model, id=id)
    elif type == 'steerableAxleModel':
        namegroup = 'Модель управляемого моста'
        item = get_object_or_404(Steerable_axle_model, id=id)
    elif type == 'ServiceCompany':
        namegroup = 'Сервисная организация'
        item = get_object_or_404(Service_company, id=id)
    return render(request, 'dict.html', {'item': item, 'namegroup' : namegroup, 'type' : type})

def maintenance_directory (request, id, type):
    if type == 'typeMaintenance':
        namegroup = 'Вид ТО'    
        item = get_object_or_404(Type_maintenance, id=id)
    elif type == 'serviceCompany':
        namegroup = 'Сервисная организация'
        item = get_object_or_404(Service_company, id=id)
    elif type == 'organizationMaintenance':
        namegroup = 'Организация, проводившая ТО'
        item = get_object_or_404(Organization_maintenance, id=id) 
    return render(request, 'dict.html', {'item': item, 'namegroup' : namegroup, 'type' : type})

def complaint_directory (request, id, type):
    if type == 'failureNode':
        namegroup = 'Узел отказа'
        item = get_object_or_404(Failure_node, id=id)
    elif type == 'recoveryMethod':
        namegroup = 'Способ восстановления'
        item = get_object_or_404(Recovery_method, id=id)
    elif type == 'serviceCompany':
        namegroup = 'Сервисная организация'
        item = get_object_or_404(Service_company, id=id)
    return render(request, 'dict.html', {'item': item, 'namegroup' : namegroup, 'type' : type})
                
# Клиент имеет доступ к данным определённых машин. У каждой машины есть только один клиент.
# Сервисная организация имеет доступ к данным определённых машин. У каждой машины только одна сервисная организация.
# Менеджер имеет доступ к данным по всем машинам, а также имеет возможность редактировать справочники.

class CarListView(LoginRequiredMixin, ListView):
    model = Car
    template_name = 'cars.html'
    ordering = 'shipping_date'         
    context_object_name = 'cars'
    paginate_by = 5
    login_url = '/accounts/login/'


class CarDetailView(DetailView):
    model = Car
    template_name = 'car_detail.html'                              
    context_object_name = 'car'


class MaintenanceListView(PermissionRequiredMixin, ListView): 
    model = Maintenance
    ordering = 'order_date'
    template_name = 'maintenance/maintenances.html'                 
    permission_required = ('silant.view_maintenance',)
    context_object_name = 'maintenances'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            if self.request.user.has_perm('silant.view_maintenance_noclient') == False: 
                queryset = Maintenance.objects.filter(car__client__user=self.request.user)
            else:
                if self.request.user.has_perm('silant.view_maintenance_noservice') == False:
                    queryset = Maintenance.objects.filter(service_company__user=self.request.user)
            self.filterset = MaintenanceFilter(self.request.GET, queryset)
        else:
            if not bool(self.request.GET):
                queryset = Maintenance.objects.none()
        return self.filterset.qs
      
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context
    

class MaintenanceCreateView(PermissionRequiredMixin, CreateView):
    model = Maintenance
    form_class = MaintenanceForm
    template_name = 'maintenance/create_maintenance.html'
    permission_required = ('silant.add_maintenance',)
    success_url = '/cars/maintenances/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class MaintenanceUpdateView(PermissionRequiredMixin, UpdateView):
    model = Maintenance
    form_class = MaintenanceForm
    template_name = 'maintenance/create_maintenance.html'         
    permission_required = ('silant.change_maintenance', )
    success_url = '/cars/maintenances/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


def create_or_update_maintenance(request, pk=None):
    if pk:
        view_class = MaintenanceUpdateView.as_view()
    else:
        view_class = MaintenanceCreateView.as_view()

    return view_class(request, pk=pk)
    

class ComplaintsListView(LoginRequiredMixin, ListView): 
    model = Complaints
    form_class = ComplaintsForm
    ordering = 'date_of_refusal'
    template_name = 'complaints/complaints.html'                 
    permission_required = ('silant.view_complaints',)
    context_object_name = 'complaints'
    paginate_by = 10
    
    # Если пользователь аутентифицирован и проходит по правам, то он может просматривать все жалобы. Админ и бог
    # Если не админ, но залогинился, то может просматривать только жалобы, относящиеся к его клиентам. 
    # Если пользователь не аутентифицирован или если запрос не содержит параметров фильтра, то набор данных пустой.
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_authenticated:
            if self.request.user.has_perm('silant.view_complaints_noclient') == False: 
                queryset = Complaints.objects.filter(car__client__user=self.request.user)
            else:
                if self.request.user.has_perm('silant.view_complaints_noservice') == False:
                    queryset = Complaints.objects.filter(service_company__user=self.request.user)
            self.filterset = ComplaintsFilter(self.request.GET, queryset)
        else:
            if not bool(self.request.GET):
                queryset = Complaints.objects.none()
        return self.filterset.qs
      
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context
    

class ComplaintsCreateView(PermissionRequiredMixin, CreateView):
    model = Complaints
    form_class = ComplaintsForm
    template_name = 'complaints/create_complaints.html'                   
    permission_required = ('silant.add_complaints',)
    success_url = '/cars/complaints/'

    def form_valid(self, form): 
         self.object = form.save(commit=False)
         self.object.user = self.request.user
         self.object.save()
         return redirect(self.get_success_url())
    

class ComplaintsUpdateView(PermissionRequiredMixin, UpdateView):
    form_class = ComplaintsForm
    model = Complaints
    template_name = 'complaints/create_complaints.html'                   
    permission_required = ('silant.change_complaints', )
    success_url = '/cars/complaints/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return redirect(self.get_success_url())
    
    def save_dictionary(self, request): 
        if request.method == 'POST':          # эта проверка, чтобы не было случайного или 'случайного' изменения данных через GET-запросы))
            print(request.POST)
            id = request.POST['id']
            type = request.POST['type']
            name = request.POST['name']
            description = request.POST['description']
            if type == 'techniqueModel':
                model = Technique_model.objects.get(id=id)
                model.name = name
                model.description = description
                model.save()
            elif type == 'engineModel':
                model = Engine_model.objects.get(id=id)
                model.name = name
                model.description = description
                model.save()
            elif type == 'transmissionModel':
                model = Transmission_model.objects.get(id=id)
                model.name = name
                model.description = description
                model.save()
            elif type == 'driveAxleModel':
                model = Drive_axle_model.objects.get(id=id)
                model.name = name
                model.description = description
                model.save()
            elif type == 'steerableAxleModel':
                model = Steerable_axle_model.objects.get(id=id)
                model.name = name
                model.description = description
                model.save()
            elif type == 'ServiceCompany':
                model = Service_company.objects.get(id=id)
                model.name = name
                model.description = description
                model.save()                    
            elif type == 'typeMaintenance':
                model = Type_maintenance.objects.get(id=id)
                model.name = name
                model.description = description
                model.save()
            elif type == 'organizationMaintenance':
                model = Organization_maintenance.objects.get(id=id)
                model.name = name
                model.description = description
                model.save()
            elif type == 'failureNode':
                model = Failure_node.objects.get(id=id)
                model.name = name
                model.description = description
                model.save()
            elif type == 'recoveryMethod':
                model = Recovery_method.objects.get(id=id)
                model.name = name
                model.description = description
                model.save()      

            return redirect('/')
    

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})
