from django.contrib import admin
from information.models import Passenger


class PassengerAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullname', 'flight', 'flight_date', 'departure_city', 'arrival_city', 'seat', 'baggage',
                    'id_type', 'id_number', 'dialling_code', 'telephone', 'inbound_country',
                    'inbound_flight', 'inbound_date', 'quarantine_end', 'body_temperature', 'healthy_code',
                    'address', 'verifier')
    search_fields = ('flight',)
    filter = ('flight_date',)


class PassengerListAdmin(admin.ModelAdmin):
    change_list_template = "admin/man_hour_summary_change_list.html"

    list_display = ('id', 'file_name', 'success', 'failure', 'upload_datetime')
    search_fields = ('file_name',)
    filter = ('upload_datetime',)


admin.site.register(Passenger, PassengerAdmin)
