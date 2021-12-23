from django.shortcuts import render
from quickcheck.models import Province, City


def quickcheck(request):
    provinces = list(Province.objects.all().values_list('name', flat=True))
    city_contents = {}
    cities = City.objects.all()
    for province in provinces:
        city_contents[province] = list(cities.filter(province__name=province).values('id', 'name', 'summary', 'policy', 'image', 'update_datetime'))
    for value in city_contents.values():
        for item in value:
            item['policy'] = {v.split('-')[0]: v.split('-')[1:] for v in item['policy'].replace('\r\n', '').split('*') if v != ''}
    last_update_datetime = cities.order_by('-update_datetime').first().update_datetime
    return render(request, 'quickcheck.html', {'city_contents': city_contents, 'last_update_datetime': last_update_datetime})
