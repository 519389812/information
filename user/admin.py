from django.contrib import admin
from user.models import CustomUser, Verifier
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.core.validators import validate_email
import re


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('个人信息', {'fields': ('first_name', 'last_name', 'full_name')}),
        ('权限', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('其他信息', {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'full_name', 'is_active', 'is_staff', 'is_superuser')
    list_editable = ('is_active', 'is_staff', 'is_superuser')
    readonly_fields = ('full_name',)
    filter_horizontal = ('groups', 'user_permissions', )
    search_fields = ('full_name',)

    def save_model(self, request, obj, form, change):
        if form.is_valid():
            if not change:
                super().save_model(request, obj, form, change)
            if 'email' in form.cleaned_data.keys():
                if form.cleaned_data['email']:
                    if validate_email(obj.email):
                        messages.error(request, "保存失败，邮箱格式不合法！")
                        messages.set_level(request, messages.ERROR)
                        return
                    email_before = CustomUser.objects.get(id=obj.id).email
                    email_after = form.cleaned_data['email']
                    if email_before != email_after:
                        obj.email_verify = False
            super().save_model(request, obj, form, change)


class VerifierAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'code')
    search_fields = ('user__full_name',)
    autocomplete_fields = ('user',)

    def get_form(self, request, obj=None, **kwargs):
        help_texts = {
            'code': '请设置【4】位纯数字验证码',
        }
        kwargs.update({'help_texts': help_texts})
        return super(VerifierAdmin, self).get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        if form.is_valid():
            code = form.cleaned_data['code']
            if form.cleaned_data['code']:
                if not re.search(r'^\d{4}$', code):
                    messages.error(request, "保存失败，请设置【4】位纯数字验证码！")
                    messages.set_level(request, messages.ERROR)
                    return
            super().save_model(request, obj, form, change)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Verifier, VerifierAdmin)


admin.site.site_header = '信息采集系统'
admin.site.site_title = '信息采集系统'
admin.site.index_title = '信息采集系统'
