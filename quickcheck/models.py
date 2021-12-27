from django.db import models
from user.models import CustomUser
from InformationCollector.safe import aes_encrypt, aes_decrypt
from InformationCollector.settings import AES_KEY, AES_VI
import base64


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
    summary = models.TextField(max_length=1000, verbose_name='概览', editable=True)
    summary_enc = models.BooleanField(default=False)
    policy = models.TextField(max_length=10000, verbose_name='详细政策', editable=True)
    policy_enc = models.BooleanField(default=False)
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

    def __getattribute__(self, attr):
        try:
            if attr in object.__getattribute__(self, 'encrypt_items') and (object.__getattribute__(self, '%s_enc' % attr)):
                return aes_decrypt(AES_KEY, object.__getattribute__(self, attr), AES_VI)
            else:
                return object.__getattribute__(self, attr)
        except Exception as e:
            raise e

    def save(self, *args, **kwargs):
        print(self.summary_enc)
        if not self.summary_enc:
            print(self.summary_enc)
            self.summary = aes_encrypt(AES_KEY, self.summary, AES_VI)
            print(self.summary)
            self.summary_enc = True
        if not self.policy_enc:
            self.policy = aes_encrypt(AES_KEY, self.policy, AES_VI)
            self.policy_enc = True
        # for attr in self.encrypt_items:
        #     if not eval('self.%s_enc' % attr):
        #         self.__setattr__(attr, aes_encrypt(AES_KEY, eval('self.%s' % attr), AES_VI))
        #         self.__setattr__('%s_enc' % attr, True)
        super().save(*args, **kwargs)
