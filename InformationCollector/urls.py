"""InformationCollector URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from InformationCollector import views as m_view
from information import views as i_view
from quickcheck import views as q_view
from user import views as u_view
from django.conf.urls.static import static
from . import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', m_view.home, name="home"),

    path('login/', u_view.login, name="login"),
    path('logout/', u_view.logout, name="logout"),
    path('pax/', i_view.collect_pax, name='collect_pax'),
    path('export_pax/', i_view.export_pax, name='export_pax'),
    path('save_pax/', i_view.save_pax, name='save'),

    # passenger form validate
    path('check_fullname_validate/', i_view.check_fullname_validate, name="check_fullname_validate"),
    path('check_flight_validate/', i_view.check_flight_validate, name="check_flight_validate"),
    path('check_flight_date_validate/', i_view.check_flight_date_validate, name="check_flight_date_validate"),
    path('check_departure_validate/', i_view.check_departure_validate, name="check_departure_validate"),
    path('check_arrival_validate/', i_view.check_arrival_validate, name="check_arrival_validate"),
    path('check_seat_validate/', i_view.check_seat_validate, name="check_seat_validate"),
    path('check_baggage_validate/', i_view.check_baggage_validate, name="check_baggage_validate"),
    path('check_id_type_validate/', i_view.check_id_type_validate, name="check_id_type_validate"),
    path('check_id_number_validate/', i_view.check_id_number_validate, name="check_id_number_validate"),
    path('check_dialling_code_validate/', i_view.check_dialling_code_validate, name="check_dialling_code_validate"),
    path('check_telephone_validate/', i_view.check_telephone_validate, name="check_telephone_validate"),
    path('check_inbound_country_validate/', i_view.check_inbound_country_validate, name="check_inbound_country_validate"),
    path('check_inbound_flight_validate/', i_view.check_inbound_flight_validate, name="check_inbound_flight_validate"),
    path('check_inbound_date_validate/', i_view.check_inbound_date_validate, name="check_inbound_date_validate"),
    path('check_quarantine_end_validate/', i_view.check_quarantine_end_validate, name="check_quarantine_end_validate"),
    path('check_body_temperature_validate/', i_view.check_body_temperature_validate, name="check_body_temperature_validate"),
    path('check_healthy_code_validate/', i_view.check_healthy_code_validate, name="check_healthy_code_validate"),
    path('check_address_validate/', i_view.check_address_validate, name="check_address_validate"),
    path('check_code_validate/', i_view.check_code_validate, name="check_code_validate"),
    # re_path(r'check_verify_email/(.*)/$', user_views.check_verify_email, name="check_verify_email"),

    # done
    path('done/', i_view.show_done, name='show_done'),

    # quickcheck
    path('quickcheck/', q_view.quickcheck, name='quickcheck'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
