from django.contrib import admin
from information.models import Passenger


class PassengerAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullname', 'flight', 'flight_date', 'departure_city', 'arrival_city', 'seat', 'baggage',
                    'id_type', 'id_number', 'dialling_code', 'telephone', 'inbound_country',
                    'inbound_flight', 'inbound_date', 'quarantine_end', 'body_temperature', 'healthy_code',
                    'address', 'verifier')
    search_fields = ('flight',)
    filter = ('flight_date', )


admin.site.register(Passenger, PassengerAdmin)
