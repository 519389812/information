from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=300, null=True, blank=True, verbose_name='全名')

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        self.full_name = '%s%s' % (self.last_name, self.first_name)
        super(CustomUser, self).save(*args, **kwargs)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
        ordering = ['full_name']


class Verifier(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, verbose_name='用户')
    code = models.CharField(max_length=30, verbose_name='验证码')

    def __str__(self):
        return self.user.full_name

    class Meta:
        verbose_name = '验证码设置'
        verbose_name_plural = '验证码设置'
