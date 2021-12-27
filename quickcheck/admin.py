from django.contrib import admin
from quickcheck.models import Province, City


class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'province', 'name', 'summary', 'update_datetime', 'update_user')
    search_fields = ('province__name', 'name')
    readonly_fields = ('update_user', )
    filter = ('update_datetime', )
    ordering = ('province', )
    exclude = ('summary_enc', 'policy_enc')

    # 必须要写入readonly_fields，否则报错
    # def basic_score(self, obj):
    #     return obj.reward.score
    # basic_score.short_description = '基础分数'

    def get_form(self, request, obj=None, **kwargs):
        help_texts = {
            'policy': '请按以下格式输入：<br/>*标题1<br/>-正文1...<br/>-正文2...<br/>*标题2<br/>...',
        }
        kwargs.update({'help_texts': help_texts})
        return super(CityAdmin, self).get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        if form.is_valid():
            obj.update_user = request.user
            super(CityAdmin, self).save_model(request, obj, form, change)


admin.site.register(Province, ProvinceAdmin)
admin.site.register(City, CityAdmin)
