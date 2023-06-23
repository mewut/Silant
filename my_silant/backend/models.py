from django.db import models
from django.contrib.auth.models import User


class Base_dictionary(models.Model):
    name = models.TextField(unique=True, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        abstract = True
        
    def __str__(self):
        return f'{self.name}'
    

class Technique_model(Base_dictionary):
    class Meta:
        verbose_name = 'Модель техники'
        verbose_name_plural = 'Модели техники'


class Engine_model(Base_dictionary):
    class Meta:
        verbose_name = 'Модель двигателя'
        verbose_name_plural = 'Модели двигателя'


class Transmission_model(Base_dictionary):
    class Meta:
        verbose_name = 'Модель трансмиссии'
        verbose_name_plural = 'Модели трансмиссии'


class Drive_axle_model(Base_dictionary):
    class Meta:
        verbose_name = 'Модель ведущего моста'
        verbose_name_plural = 'Модели ведущего моста'


class Steerable_axle_model(Base_dictionary):
    class Meta:
        verbose_name = 'Модель управляемого моста'
        verbose_name_plural = 'Модели управляемого моста'


class Service_company(Base_dictionary):
    class Meta:
        verbose_name = 'Сервисная компания'
        verbose_name_plural = 'Сервисные компании'

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Имя пользователя')


class Client(Base_dictionary):
    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Имя пользователя')
    

class Car(models.Model):
    serial_number = models.TextField(max_length=55, unique=True, db_index=True, verbose_name='Зав. № машины')
    technique_model = models.ForeignKey(Technique_model, on_delete=models.CASCADE, db_index=True, verbose_name='Модель техники')
    engine_model = models.ForeignKey(Engine_model, on_delete=models.CASCADE, db_index=True, verbose_name='Модель двигателя')
    engine_number = models.TextField(max_length=55, verbose_name='Зав. № двигателя')
    transmission_model = models.ForeignKey(Transmission_model, on_delete=models.CASCADE, db_index=True, verbose_name='Модель трансмиссии')
    transmission_number = models.TextField(max_length=55, verbose_name='Зав. № трансмиссии')
    drive_axle_model = models.ForeignKey(Drive_axle_model, on_delete=models.CASCADE, db_index=True, verbose_name='Модель ведущего моста')
    drive_axle_number = models.TextField(max_length=55, verbose_name='Зав. № ведущего моста')
    steerable_axle_model = models.ForeignKey(Steerable_axle_model, on_delete=models.CASCADE, db_index=True, verbose_name='Модель управляемого моста')
    steerable_axle_number = models.TextField(max_length=55, verbose_name='Зав. № управляемого моста')
    supply_contract = models.TextField(max_length=55, blank=True, verbose_name='Договор поставки №, дата.')
    shipping_date = models.DateField(db_index=True, verbose_name='Дата отгрузки с завода')
    consignee = models.TextField(max_length=55, blank=True, verbose_name='Грузополучатель (конечный потребитель)')
    delivery_address = models.TextField(max_length=255, blank=True, verbose_name='Адрес поставки (эксплуатации)')
    equipment = models.TextField(max_length=255, blank=True, verbose_name='Комплектация (доп. опции)')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Клиент')
    service_company = models.ForeignKey(Service_company, on_delete=models.CASCADE, blank=True, verbose_name='Сервисная организация')

    def __str__(self):
        return f'{self.serial_number}'

    class Meta:
        verbose_name = 'Машины'
        verbose_name_plural = 'Машины'
        ordering = ['shipping_date']
        # права просмотра
        permissions = ( 
            ('view_car_noclient', 'Can view no client'),
            ('view_car_noservice', 'Can view no service')
        )    
        

class Type_maintenance(Base_dictionary):
    class Meta:
        verbose_name = 'Вид ТО'
        verbose_name_plural = 'Виды ТО'


class Organization_maintenance(Base_dictionary):
    class Meta:
         verbose_name = 'Организация, проводившая ТО'
         verbose_name_plural = 'Организации, проводившие ТО'


class Maintenance(models.Model):
    type_maintenance = models.ForeignKey(Type_maintenance, on_delete=models.CASCADE, verbose_name='Вид ТО')
    maintenance_date = models.DateField(verbose_name='Дата проведения ТО')
    operating_time = models.IntegerField(verbose_name='Наработка м/час')
    order = models.TextField(max_length=55, verbose_name='Номер заказа-наряда')
    order_date = models.DateField(verbose_name='Дата заказа-наряда')
    organization_maintenance = models.ForeignKey(Organization_maintenance, on_delete=models.CASCADE, verbose_name='Организация, проводившая ТО')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name='Машина')
    service_company = models.ForeignKey(Service_company, on_delete=models.CASCADE,verbose_name='Сервисная компания')

    def __str__(self):
        return f'{self.car}'

    class Meta:
        verbose_name = 'ТО'
        verbose_name_plural = 'ТО'      
        ordering = ['maintenance_date']
        # права просмотра
        permissions = (
            ('view_maintenance_noclient', 'maintenance view no client'),
            ('view_maintenance_noservice', 'Can view no service')
        )


class Failure_node(Base_dictionary):
    class Meta:
        verbose_name = 'Узел отказа'
        verbose_name_plural = 'Узлы отказа'


class Recovery_method(Base_dictionary):
    class Meta:
        verbose_name = 'Способ восстановления'
        verbose_name_plural = 'Способы восстановления'


class Complaints(models.Model):
    date_of_refusal = models.DateField(verbose_name='Дата отказа')
    operating_time = models.IntegerField(verbose_name='Наработка м/час')
    failure_node = models.ForeignKey(Failure_node, on_delete=models.CASCADE, verbose_name='Узел отказа') 
    description_failure = models.TextField(max_length=1024, verbose_name='Характер отказа')
    recovery_method = models.ForeignKey(Recovery_method, on_delete=models.CASCADE, verbose_name='Способ восстановления')
    parts_used = models.TextField(verbose_name='Используемые запасные части')
    date_of_restoration = models.DateField(verbose_name='Дата восстановления') 
    equipment_downtime = models.IntegerField(verbose_name='Время простоя техники', null = True, blank=True, editable=False)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name='Машина')
    service_company = models.ForeignKey(Service_company, on_delete=models.CASCADE, verbose_name='Сервисная организация')

    def __str__(self):
        return f'{self.car}'

    class Meta:
        verbose_name = 'Рекламации'
        verbose_name_plural = 'Рекламации'
        ordering = ['date_of_refusal']
        # права просмотра
        permissions = ( 
            ('view_complaints_noclient', 'complaints view no client'),
            ('view_complaints_noservice', 'Can view no service')
        )

    # Расчетное поле для времени простоя техники: Дата восстановления - Дата отказа
    def save(self, *args, **kwargs):
        self.equipment_downtime = (self.date_of_restoration - self.date_of_refusal).days
        super(Complaints, self).save(*args, **kwargs)
