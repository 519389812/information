# Generated by Django 3.2.9 on 2021-12-27 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Passenger',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('fullname', models.CharField(blank=True, max_length=100, verbose_name='姓名')),
                ('flight', models.CharField(blank=True, max_length=50, verbose_name='航班号')),
                ('flight_date', models.DateField(blank=True, verbose_name='起飞时间')),
                ('departure_city', models.CharField(blank=True, max_length=50, verbose_name='起飞地')),
                ('arrival_city', models.CharField(blank=True, max_length=50, verbose_name='目的地')),
                ('seat', models.CharField(blank=True, max_length=20, verbose_name='座位号')),
                ('baggage', models.CharField(blank=True, max_length=10, verbose_name='托运行李件数')),
                ('id_type', models.CharField(blank=True, max_length=30, verbose_name='证件类别')),
                ('id_number', models.CharField(blank=True, max_length=30, verbose_name='证件号')),
                ('dialling_code', models.CharField(blank=True, max_length=20, verbose_name='联系电话区号')),
                ('telephone', models.CharField(blank=True, max_length=30, verbose_name='联系电话')),
                ('inbound_country', models.CharField(blank=True, max_length=100, verbose_name='入境国家')),
                ('inbound_flight', models.CharField(blank=True, max_length=30, verbose_name='入境航班号')),
                ('inbound_date', models.DateField(blank=True, verbose_name='入境时间')),
                ('quarantine_end', models.DateField(blank=True, verbose_name='解除隔离时间')),
                ('body_temperature', models.FloatField(blank=True, verbose_name='体温状态')),
                ('healthy_code', models.CharField(blank=True, max_length=10, verbose_name='健康码')),
                ('address', models.TextField(blank=True, max_length=1000, verbose_name='目的地详细地址')),
            ],
            options={
                'verbose_name': 'pax信息',
                'verbose_name_plural': 'pax信息',
            },
        ),
    ]
