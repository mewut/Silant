from django import forms
from .models import Car, Client, Complaints, Drive_axle_model, Engine_model, Failure_node, Maintenance, Organization_maintenance, Recovery_method, Service_company, Steerable_axle_model, Technique_model, Transmission_model, Type_maintenance
from django.utils import timezone

now = timezone.now()

class CarForm(forms.ModelForm):
    technique_model = forms.ModelChoiceField(queryset=Technique_model.objects.all(), label='Модель техники', widget=forms.Select(attrs={"class":"form-control text-black text-center"}))
    engine_model = forms.ModelChoiceField(queryset=Engine_model.objects.all(), label='Модель двигателя', widget=forms.Select(attrs={"class":"form-control text-black text-center"}))
    transmission_model = forms.ModelChoiceField(queryset=Transmission_model.objects.all(), label='Модель трансмиссии', widget=forms.Select(attrs={"class":"form-control text-black text-center"}))
    drive_axle_model = forms.ModelChoiceField(queryset=Drive_axle_model.objects.all(), label='Модель ведущего моста', widget=forms.Select(attrs={"class":"form-control text-black text-center"}))
    steerable_axle_model = forms.ModelChoiceField(queryset=Steerable_axle_model.objects.all(), label='Модель управляемого моста', widget=forms.Select(attrs={"class":"form-control text-black text-center"}))
    client = forms.ModelChoiceField(queryset=Client.objects.all(), label='Клиент', widget=forms.Select(attrs={"class":"form-control text-black text-center"}))
    service_company = forms.ModelChoiceField(queryset=Service_company.objects.all(), label='Сервисная организация', widget=forms.Select(attrs={"class":"form-control text-black text-center"}))  
    class Meta:
        model = Car
        widgets = {'serial_number': forms.Textarea(attrs={"rows": 1,"class":"form-control text-black text-center"}),
                    'engine_number': forms.Textarea(attrs={"rows": 1,"class":"form-control text-black text-center"}),
                    'transmission_number': forms.Textarea(attrs={"rows": 1,"class":"form-control text-black text-center"}),
                    'drive_axle_number': forms.Textarea(attrs={"rows": 1,"class":"form-control text-black text-center"}),
                    'steerable_axle_number': forms.Textarea(attrs={"rows": 1,"class":"form-control text-black text-center"}),
                    'supply_contract': forms.Textarea(attrs={"rows": 1,"class":"form-control text-black text-center"}),
                    'consignee': forms.Textarea(attrs={"rows": 1,"class":"form-control text-black text-center"}),
                    'delivery_address': forms.Textarea(attrs={"rows": 1,"class":"form-control text-black text-center"}),
                    'equipment': forms.Textarea(attrs={"rows": 1,"class":"form-control text-black text-center"}),
                    'shipping_date': forms.TextInput(attrs={'type': 'date'})  
                }
        fields = '__all__'


class MaintenanceForm(forms.ModelForm):
    type_maintenance = forms.ModelChoiceField(queryset=Type_maintenance.objects.all(), label='Вид ТО', widget=forms.Select(attrs={"class":"form-control text-black text-center"}))
    organization_maintenance = forms.ModelChoiceField (queryset=Organization_maintenance.objects.all(), label='Организация, проводившая ТО', widget=forms.Select(attrs={"class":"form-control text-black text-center"}))
    car = forms.ModelChoiceField (queryset=Car.objects.all(), label='Машина', widget=forms.Select(attrs={"class":"form-control text-black text-center"}))
    service_company = forms.ModelChoiceField (queryset=Service_company.objects.all(), label='Сервисная организация', widget=forms.Select(attrs={"class":"form-control text-black text-center"}))
    operating_time = forms.IntegerField (min_value=0, label='Наработка м/час', widget=forms.NumberInput (attrs={"class":"form-control text-black text-center"}))
    class Meta:
        model = Maintenance
        widgets = {'maintenance_date': forms.SelectDateWidget(years=list(reversed(range(2000, now.year+1))), attrs={"rows": 1,"class":"form-control text-black text-center"}),
                   'order': forms.Textarea(attrs={"rows": 1,"class":"form-control text-black text-center"}),
                   'order_date': forms.SelectDateWidget(years=list(reversed(range(2000, now.year+1))), attrs={"rows": 1,"class":"form-control text-black text-center"}),
                }
        fields = '__all__'


class ComplaintsForm(forms.ModelForm):
    operating_time = forms.IntegerField (min_value=0, label='Наработка м/час', widget=forms.NumberInput (attrs={"class":"form-control text-black text-center"}))
    failure_node = forms.ModelChoiceField(queryset=Failure_node.objects.all(), label='Узел отказа', widget=forms.Select(attrs={"class":"form-control text-black text-center"}))
    recovery_method = forms.ModelChoiceField(queryset=Recovery_method.objects.all(), label='Способ восстановления', widget=forms.Select(attrs={"class":"form-control text-black text-center"}))
    car = forms.ModelChoiceField (queryset=Car.objects.all(), label='Машина', widget=forms.Select(attrs={"class":"form-control text-black text-center"}))
    service_company = forms.ModelChoiceField (queryset=Service_company.objects.all(), label='Сервисная организация', widget=forms.Select(attrs={"class":"form-control text-black text-center"}))
    class Meta:
        model = Complaints
        widgets = {'date_of_refusal': forms.SelectDateWidget(years=list(reversed(range(2000, now.year+1))), attrs={"rows": 1,"class":"form-control text-black text-center"}),
                   'description_failure': forms.Textarea(attrs={'rows': 1,"class":"form-control text-black text-center"}),
                   'parts_used': forms.Textarea(attrs={'rows': 1,"class":"form-control text-black text-center"}),
                   'date_of_restoration': forms.SelectDateWidget(years=list(reversed(range(2000, now.year+1))), attrs={"rows": 1,"class":"form-control text-black text-center"}),
                }
        fields = '__all__'
