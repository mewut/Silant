from django.db import models
from django.contrib.auth.models import User


# class Base_dictionary(models.Model):
#     name = models.TextField(unique=True, verbose_name='Название')
#     description = models.TextField(blank=True, verbose_name='Описание')

#     class Meta:
#         abstract = True
        
#     def __str__(self):
#         return f'{self.name}'
    

class TechniqueModel(models.Model):
    name = models.TextField(verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    def get_absolute_url(self):
        return f'/modeltech'

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Модель техники'
        verbose_name_plural = 'Модели техники'


class EngineModel(models.Model):
    name = models.TextField(verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    def get_absolute_url(self):
        return f'/modeleng'

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Модель двигателя'
        verbose_name_plural = 'Модели двигателя'


class TransmissionModel(models.Model):
    name = models.TextField(verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    def get_absolute_url(self):
        return f'/modeltrans'

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Модель трансмиссии'
        verbose_name_plural = 'Модели трансмиссии'


class DriveAxleModel(models.Model):
    name = models.TextField(verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    def get_absolute_url(self):
        return f'/modelaxel'

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Модель ведущего моста'
        verbose_name_plural = 'Модели ведущего моста'


class SteerableAxleModel(models.Model):
    name = models.TextField(verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    def get_absolute_url(self):
        return f'/modelsteer'

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Модель управляемого моста'
        verbose_name_plural = 'Модели управляемого моста'


class ServiceCompany(models.Model):
    name = models.TextField(verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    def get_absolute_url(self):
        return f'/servisecomp'

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Сервисная компания'
        verbose_name_plural = 'Сервисные компании'
    

class Client(models.Model):
    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Имя пользователя')


class Car(models.Model):
    serial_number = models.TextField(max_length=55, unique=True, db_index=True, null=True, blank=True, verbose_name='Зав. № машины')
    technique_model = models.ForeignKey(TechniqueModel, on_delete=models.CASCADE, db_index=True, null=True, blank=True, verbose_name='Модель техники')
    engine_model = models.ForeignKey(EngineModel, on_delete=models.CASCADE, db_index=True, null=True, blank=True, verbose_name='Модель двигателя')
    engine_number = models.TextField(max_length=55, null=True, blank=True, verbose_name='Зав. № двигателя')
    transmission_model = models.ForeignKey(TransmissionModel, on_delete=models.CASCADE, db_index=True, null=True, blank=True, verbose_name='Модель трансмиссии')
    transmission_number = models.TextField(max_length=55, null=True, blank=True, verbose_name='Зав. № трансмиссии')
    drive_axle_model = models.ForeignKey(DriveAxleModel, on_delete=models.CASCADE, db_index=True, null=True, blank=True, verbose_name='Модель ведущего моста')
    drive_axle_number = models.TextField(max_length=55, verbose_name='Зав. № ведущего моста')
    steerable_axle_model = models.ForeignKey(SteerableAxleModel, on_delete=models.CASCADE, db_index=True, null=True, blank=True, verbose_name='Модель управляемого моста')
    steerable_axle_number = models.TextField(max_length=55, null=True, blank=True, verbose_name='Зав. № управляемого моста')
    supply_contract = models.TextField(max_length=55, null=True, blank=True, verbose_name='Договор поставки №, дата.')
    shipping_date = models.DateField(db_index=True, null=True, blank=True, verbose_name='Дата отгрузки с завода')
    consignee = models.TextField(max_length=55, null=True, blank=True, verbose_name='Грузополучатель (конечный потребитель)')
    delivery_address = models.TextField(max_length=255, null=True, blank=True, verbose_name='Адрес поставки (эксплуатации)')
    equipment = models.TextField(max_length=255, null=True, blank=True, verbose_name='Комплектация (доп. опции)')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Клиент')
    service_company = models.ForeignKey(ServiceCompany, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Сервисная организация')

    def __str__(self):
        return f'{self.serial_number}'
    
    def get_absolute_url(self):
        return f'/user'

    class Meta:
        verbose_name = 'Машины'
        verbose_name_plural = 'Машины'
        ordering = ['-shipping_date'] # Сортировка по дате отгрузки
        

class TypeMaintenance(models.Model):
    name = models.TextField(verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    def get_absolute_url(self):
        return f'/maintenancetype'

    def __str__(self):
        return self.name


class OrganizationMaintenance(models.Model):
    name = models.TextField(verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    def get_absolute_url(self):
        return f'/maintenanceorg'

    def __str__(self):
        return self.name
    
    class Meta:
         verbose_name = 'Организация, проводившая ТО'
         verbose_name_plural = 'Организации, проводившие ТО'


class Maintenance(models.Model):
    type_maintenance = models.ForeignKey(TypeMaintenance, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Вид ТО')
    maintenance_date = models.DateField(null=True, blank=True, verbose_name='Дата проведения ТО')
    operating_time = models.IntegerField(null=True, blank=True, verbose_name='Наработка м/час')
    order = models.TextField(max_length=55, null=True, blank=True, verbose_name='Номер заказа-наряда')
    order_date = models.DateField(verbose_name='Дата заказа-наряда')
    organization_maintenance = models.ForeignKey(OrganizationMaintenance, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Организация, проводившая ТО')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Машина')
    service_company = models.ForeignKey(ServiceCompany, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Сервисная компания')
    serial_number = models.TextField(max_length=55, unique=True, db_index=True, null=True, blank=True, verbose_name='Зав. № машины')

    def __str__(self):
        return f'{self.car}'
    
    def get_absolute_url(self):
        return f'/maintenance'

    class Meta:
        verbose_name = 'ТО'
        verbose_name_plural = 'ТО'      
        ordering = ['-maintenance_date']


class FailureNode(models.Model):
    name = models.TextField(verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    def get_absolute_url(self):
        return f'/fnode'

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Узел отказа'
        verbose_name_plural = 'Узлы отказа'


class RecoveryMethod(models.Model):
    name = models.TextField(verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    def get_absolute_url(self):
        return f'/reco'

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Способ восстановления'
        verbose_name_plural = 'Способы восстановления'


class Complaints(models.Model):
    date_of_refusal = models.DateField(null=True, blank=True, verbose_name='Дата отказа')
    operating_time = models.IntegerField(null=True, blank=True, verbose_name='Наработка м/час')
    failure_node = models.ForeignKey(FailureNode, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Узел отказа') 
    description_failure = models.TextField(max_length=1024, null=True, blank=True, verbose_name='Характер отказа')
    recovery_method = models.ForeignKey(RecoveryMethod, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Способ восстановления')
    parts_used = models.TextField(verbose_name='Используемые запасные части', null=True, blank=True)
    date_of_restoration = models.DateField(verbose_name='Дата восстановления') 
    equipment_downtime = models.IntegerField(verbose_name='Время простоя техники', null=True, blank=True, editable=True)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Машина')
    service_company = models.ForeignKey(ServiceCompany, on_delete=models.CASCADE, null=True, verbose_name='Сервисная организация')
    serial_number = models.TextField(max_length=55, unique=True, db_index=True, null=True, blank=True, verbose_name='Зав. № машины')

    def __str__(self):
        return f'{self.car}'
    
    def get_absolute_url(self):
        return f'/complaints'

    class Meta:
        verbose_name = 'Рекламации'
        verbose_name_plural = 'Рекламации'
        ordering = ['-date_of_refusal']

    # Расчетное поле для времени простоя техники: Дата восстановления - Дата отказа
    def save(self, *args, **kwargs):
        self.equipment_downtime = (self.date_of_restoration - self.date_of_refusal).days
        super(Complaints, self).save(*args, **kwargs)
        # это я не переписывала, потому что оно работает
