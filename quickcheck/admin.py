from django.contrib import admin
from quickcheck.models import Province, City


class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'province__name', 'name', 'update_datetime', 'update_user__name')
    search_fields = ('province__name', 'name', 'update_user__name')
    filter = ('update_datetime', )

    def get_form(self, request, obj=None, **kwargs):
        help_texts = {
            'policy': '请按以下格式输入：\n*标题1\n-正文1\n-正文2',
        }
        kwargs.update({'help_texts': help_texts})
        return super(CityAdmin, self).get_form(request, obj, **kwargs)


admin.site.register(Province, ProvinceAdmin)
admin.site.register(City, CityAdmin)
