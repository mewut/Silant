from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import CreateView, ListView, UpdateView, DetailView
from .forms import CarForm, ComplaintsForm, MaintenanceForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from .models import *

# https://www.youtube.com/watch?v=NxBlcfJQSNk&list=PLF-NY6ldwAWrb6nQcPL21XX_-AmivFAYq&index=9&ab_channel=DjangoSchool

# СДЕЛАТЬ HTML!!! CarCreate.html   Dict.html    Cars.html   

class CarCreate(PermissionRequiredMixin, CreateView):
    model = Car
    form_class = CarForm
    template_name = 'CarCreate.html'                
    permission_required = ('silant.add_car',)
    success_url = '/cars/'                         

# и обратно в список
    def form_valid(self, form): 
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return redirect(self.get_success_url())
    

class CarEdit(PermissionRequiredMixin, UpdateView):
    form_class = CarForm
    model = Car
    template_name = 'CarCreate.html'                    
    permission_required = ('silant.change_car', )
    success_url = '/cars/'                             

# и обратно в список
    def form_valid(self, form): 
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return redirect(self.get_success_url())



# ууууфффффффффффф +_+