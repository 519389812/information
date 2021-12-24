from django.db import models
from user.models import CustomUser
from InformationCollector.safe import aes_encrypt, aes_decrypt
from InformationCollector.settings import AES_KEY, AES_VI


class Province(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=300, verbose_name='省份')

    class Meta:
        verbose_name = '省份'
        verbose_name_plural = '省份'

    def __str__(self):
        return self.name


class City(models.Model):
    id = models.AutoField(primary_key=True)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='city_province', verbose_name='省份')
    name = models.CharField(max_length=300, verbose_name='城市')
    summary = models.TextField(max_length=100, verbose_name='概览')
    policy = models.TextField(max_length=10000, verbose_name='详细政策')
    image = models.ImageField(blank=True, upload_to='quickcheck', verbose_name='图片')
    update_datetime = models.DateTimeField(auto_now=True, verbose_name='最新更新时间')
    update_user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, verbose_name='最新更新用户')

    class Meta:
        verbose_name = '城市'
        verbose_name_plural = '城市'
        # ordering = ['province']

    def __str__(self):
        return self.name

    encrypt_items = ['summary', 'policy']

    # def __getattribute__(self, attr):
    #     try:
    #         if attr in object.__getattribute__(self, 'encrypt_items'):
    #             print('undecode:', (object.__getattribute__(self, attr)))
    #             print('decode:', aes_decrypt(AES_KEY, object.__getattribute__(self, attr), AES_VI))
    #             return aes_decrypt(AES_KEY, object.__getattribute__(self, attr).strip("b'").encode(), AES_VI)
    #         else:
    #             return object.__getattribute__(self, attr)
    #     except Exception as e:
    #         pass

    def save(self, *args, **kwargs):
        for attr in self.encrypt_items:
            print('unencode:', object.__getattribute__(self, attr))
            print('encode:', aes_encrypt(AES_KEY, object.__getattribute__(self, attr), AES_VI))
            self.__setattr__(attr, aes_encrypt(AES_KEY, object.__getattribute__(self, attr), AES_VI))
        super(City, self).save(*args, **kwargs)


