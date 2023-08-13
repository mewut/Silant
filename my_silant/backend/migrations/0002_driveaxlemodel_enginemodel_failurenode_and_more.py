# Generated by Django 4.1 on 2023-08-08 09:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DriveAxleModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Модель ведущего моста',
                'verbose_name_plural': 'Модели ведущего моста',
            },
        ),
        migrations.CreateModel(
            name='EngineModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Модель двигателя',
                'verbose_name_plural': 'Модели двигателя',
            },
        ),
        migrations.CreateModel(
            name='FailureNode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Узел отказа',
                'verbose_name_plural': 'Узлы отказа',
            },
        ),
        migrations.CreateModel(
            name='OrganizationMaintenance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Организация, проводившая ТО',
                'verbose_name_plural': 'Организации, проводившие ТО',
            },
        ),
        migrations.CreateModel(
            name='RecoveryMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Способ восстановления',
                'verbose_name_plural': 'Способы восстановления',
            },
        ),
        migrations.CreateModel(
            name='ServiceCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Сервисная компания',
                'verbose_name_plural': 'Сервисные компании',
            },
        ),
        migrations.CreateModel(
            name='SteerableAxleModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Модель управляемого моста',
                'verbose_name_plural': 'Модели управляемого моста',
            },
        ),
        migrations.CreateModel(
            name='TechniqueModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Модель техники',
                'verbose_name_plural': 'Модели техники',
            },
        ),
        migrations.CreateModel(
            name='TransmissionModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Модель трансмиссии',
                'verbose_name_plural': 'Модели трансмиссии',
            },
        ),
        migrations.CreateModel(
            name='TypeMaintenance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
            ],
        ),
        migrations.RemoveField(
            model_name='service_company',
            name='user',
        ),
        migrations.AlterModelOptions(
            name='car',
            options={'ordering': ['-shipping_date'], 'verbose_name': 'Машины', 'verbose_name_plural': 'Машины'},
        ),
        migrations.AlterModelOptions(
            name='complaints',
            options={'ordering': ['-date_of_refusal'], 'verbose_name': 'Рекламации', 'verbose_name_plural': 'Рекламации'},
        ),
        migrations.AlterModelOptions(
            name='maintenance',
            options={'ordering': ['-maintenance_date'], 'verbose_name': 'ТО', 'verbose_name_plural': 'ТО'},
        ),
        migrations.AddField(
            model_name='complaints',
            name='serial_number',
            field=models.TextField(blank=True, db_index=True, max_length=55, null=True, unique=True, verbose_name='Зав. № машины'),
        ),
        migrations.AddField(
            model_name='maintenance',
            name='serial_number',
            field=models.TextField(blank=True, db_index=True, max_length=55, null=True, unique=True, verbose_name='Зав. № машины'),
        ),
        migrations.AlterField(
            model_name='car',
            name='client',
            field=models.TextField(blank=True, null=True, verbose_name='Клиент'),
        ),
        migrations.AlterField(
            model_name='car',
            name='consignee',
            field=models.TextField(blank=True, max_length=55, null=True, verbose_name='Грузополучатель (конечный потребитель)'),
        ),
        migrations.AlterField(
            model_name='car',
            name='delivery_address',
            field=models.TextField(blank=True, max_length=255, null=True, verbose_name='Адрес поставки (эксплуатации)'),
        ),
        migrations.AlterField(
            model_name='car',
            name='engine_number',
            field=models.TextField(blank=True, max_length=55, null=True, verbose_name='Зав. № двигателя'),
        ),
        migrations.AlterField(
            model_name='car',
            name='equipment',
            field=models.TextField(blank=True, max_length=255, null=True, verbose_name='Комплектация (доп. опции)'),
        ),
        migrations.AlterField(
            model_name='car',
            name='serial_number',
            field=models.TextField(blank=True, db_index=True, max_length=55, null=True, unique=True, verbose_name='Зав. № машины'),
        ),
        migrations.AlterField(
            model_name='car',
            name='shipping_date',
            field=models.DateField(blank=True, db_index=True, null=True, verbose_name='Дата отгрузки с завода'),
        ),
        migrations.AlterField(
            model_name='car',
            name='steerable_axle_number',
            field=models.TextField(blank=True, max_length=55, null=True, verbose_name='Зав. № управляемого моста'),
        ),
        migrations.AlterField(
            model_name='car',
            name='supply_contract',
            field=models.TextField(blank=True, max_length=55, null=True, verbose_name='Договор поставки №, дата.'),
        ),
        migrations.AlterField(
            model_name='car',
            name='transmission_number',
            field=models.TextField(blank=True, max_length=55, null=True, verbose_name='Зав. № трансмиссии'),
        ),
        migrations.AlterField(
            model_name='complaints',
            name='car',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.car', verbose_name='Машина'),
        ),
        migrations.AlterField(
            model_name='complaints',
            name='date_of_refusal',
            field=models.DateField(blank=True, null=True, verbose_name='Дата отказа'),
        ),
        migrations.AlterField(
            model_name='complaints',
            name='description_failure',
            field=models.TextField(blank=True, max_length=1024, null=True, verbose_name='Характер отказа'),
        ),
        migrations.AlterField(
            model_name='complaints',
            name='equipment_downtime',
            field=models.IntegerField(blank=True, null=True, verbose_name='Время простоя техники'),
        ),
        migrations.AlterField(
            model_name='complaints',
            name='operating_time',
            field=models.IntegerField(blank=True, null=True, verbose_name='Наработка м/час'),
        ),
        migrations.AlterField(
            model_name='complaints',
            name='parts_used',
            field=models.TextField(blank=True, null=True, verbose_name='Используемые запасные части'),
        ),
        migrations.AlterField(
            model_name='maintenance',
            name='car',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.car', verbose_name='Машина'),
        ),
        migrations.AlterField(
            model_name='maintenance',
            name='maintenance_date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата проведения ТО'),
        ),
        migrations.AlterField(
            model_name='maintenance',
            name='operating_time',
            field=models.IntegerField(blank=True, null=True, verbose_name='Наработка м/час'),
        ),
        migrations.AlterField(
            model_name='maintenance',
            name='order',
            field=models.TextField(blank=True, max_length=55, null=True, verbose_name='Номер заказа-наряда'),
        ),
        migrations.DeleteModel(
            name='Client',
        ),
        migrations.AlterField(
            model_name='car',
            name='drive_axle_model',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.driveaxlemodel', verbose_name='Модель ведущего моста'),
        ),
        migrations.AlterField(
            model_name='car',
            name='engine_model',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.enginemodel', verbose_name='Модель двигателя'),
        ),
        migrations.AlterField(
            model_name='car',
            name='service_company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.servicecompany', verbose_name='Сервисная организация'),
        ),
        migrations.AlterField(
            model_name='car',
            name='steerable_axle_model',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.steerableaxlemodel', verbose_name='Модель управляемого моста'),
        ),
        migrations.AlterField(
            model_name='car',
            name='technique_model',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.techniquemodel', verbose_name='Модель техники'),
        ),
        migrations.AlterField(
            model_name='car',
            name='transmission_model',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.transmissionmodel', verbose_name='Модель трансмиссии'),
        ),
        migrations.AlterField(
            model_name='complaints',
            name='failure_node',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.failurenode', verbose_name='Узел отказа'),
        ),
        migrations.AlterField(
            model_name='complaints',
            name='recovery_method',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.recoverymethod', verbose_name='Способ восстановления'),
        ),
        migrations.AlterField(
            model_name='complaints',
            name='service_company',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.servicecompany', verbose_name='Сервисная организация'),
        ),
        migrations.AlterField(
            model_name='maintenance',
            name='organization_maintenance',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.organizationmaintenance', verbose_name='Организация, проводившая ТО'),
        ),
        migrations.AlterField(
            model_name='maintenance',
            name='service_company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.servicecompany', verbose_name='Сервисная компания'),
        ),
        migrations.AlterField(
            model_name='maintenance',
            name='type_maintenance',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='backend.typemaintenance', verbose_name='Вид ТО'),
        ),
        migrations.DeleteModel(
            name='Drive_axle_model',
        ),
        migrations.DeleteModel(
            name='Engine_model',
        ),
        migrations.DeleteModel(
            name='Failure_node',
        ),
        migrations.DeleteModel(
            name='Organization_maintenance',
        ),
        migrations.DeleteModel(
            name='Recovery_method',
        ),
        migrations.DeleteModel(
            name='Service_company',
        ),
        migrations.DeleteModel(
            name='Steerable_axle_model',
        ),
        migrations.DeleteModel(
            name='Technique_model',
        ),
        migrations.DeleteModel(
            name='Transmission_model',
        ),
        migrations.DeleteModel(
            name='Type_maintenance',
        ),
    ]
