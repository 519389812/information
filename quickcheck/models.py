from django.db import models
from user.models import CustomUser
from InformationCollector.safe import aes_encrypt, aes_decrypt
from InformationCollector.settings import AES_KEY, AES_IV


class CustomEncryptField(models.TextField):
    def __init__(self, *args, **kwargs):
        super(CustomEncryptField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if value is None:
            return value
        print('to', value)
        return encrypt_if_not_encrypted(value)

    def get_prep_value(self, value):
        if value is None:
            return value
        print('get', value)
        return decrypt_if_not_decrypted(value)


def encrypt_if_not_encrypted(value):
    print(value, type(value))
    if isinstance(value, EncryptedString):
        return value
    else:
        encrypted = aes_encrypt(AES_KEY, value, AES_IV)
        return EncryptedString(encrypted)


def decrypt_if_not_decrypted(value):
    print(value, type(value))
    if isinstance(value, DecryptedString):
        return value
    else:
        encrypted = aes_decrypt(AES_KEY, value, AES_IV)
        return DecryptedString(encrypted)


class EncryptedString(str):
    pass


class DecryptedString(str):
    pass


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
    summary = CustomEncryptField(max_length=1000, verbose_name='概览')
    policy = CustomEncryptField(max_length=10000, verbose_name='详细政策')
    image = models.ImageField(blank=True, upload_to='quickcheck', verbose_name='图片')
    update_datetime = models.DateTimeField(auto_now=True, verbose_name='最新更新时间')
    update_user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, verbose_name='最新更新用户')

    class Meta:
        verbose_name = '城市'
        verbose_name_plural = '城市'
        # ordering = ['province']

    def __str__(self):
        return self.name
