from django.db import models
from user.models import CustomUser


class Province(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=300, verbose_name='省份')

    class Meta:
        verbose_name = '省份'
        verbose_name_plural = '省份'

    def __str__(self):
        return str(self.name)


class City(models.Model):
    id = models.AutoField(primary_key=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='city_province', verbose_name='省份')
    name = models.CharField(max_length=300, verbose_name='城市')
    policy = models.TextField(max_length=10000, verbose_name='政策')
    image = models.ImageField(blank=True, upload_to='quickcheck', verbose_name='图片')
    update_datetime = models.DateTimeField(auto_now=True, verbose_name='最新更新时间')
    update_user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, verbose_name='最新更新用户')

    class Meta:
        verbose_name = '城市'
        verbose_name_plural = '城市'

    def __str__(self):
        return str(self.name)
