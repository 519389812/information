from django.db import models


class Passenger(models.Model):
    id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=100, blank=True, verbose_name='姓名')
    flight = models.CharField(max_length=50, blank=True, verbose_name='航班号')
    flight_date = models.DateField(blank=True, verbose_name='起飞时间')
    departure_city = models.CharField(max_length=50, blank=True, verbose_name='起飞地')
    arrival_city = models.CharField(max_length=50, blank=True, verbose_name='目的地')
    seat = models.CharField(max_length=20, blank=True, verbose_name='座位号')
    baggage = models.CharField(max_length=10, blank=True, verbose_name='托运行李件数')
    id_type = models.CharField(max_length=30, blank=True, verbose_name='证件类别')
    id_number = models.CharField(max_length=30, blank=True, verbose_name='证件号')
    dialling_code = models.CharField(max_length=20, blank=True, verbose_name='联系电话区号')
    telephone = models.CharField(max_length=30, blank=True, verbose_name='联系电话')
    inbound_country = models.CharField(max_length=100, blank=True, verbose_name='入境国家')
    inbound_flight = models.CharField(max_length=30, blank=True, verbose_name='入境航班号')
    inbound_date = models.DateField(blank=True, verbose_name='入境时间')
    quarantine_end = models.DateField(blank=True, verbose_name='解除隔离时间')
    body_temperature = models.FloatField(blank=True, verbose_name='体温状态')
    healthy_code = models.CharField(max_length=10, blank=True, verbose_name='健康码')
    address = models.TextField(max_length=1000, blank=True, verbose_name='目的地详细地址')
    verifier = models.ForeignKey(Verifier, on_delete=models.CASCADE, verbose_name='验证')

    class Meta:
        verbose_name = 'pax信息'
        verbose_name_plural = 'pax信息'

    def __str__(self):
        return str(self.id)