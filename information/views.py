from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, reverse, redirect
from django.utils.datastructures import MultiValueDictKeyError
import re
from information.models import Passenger
from user.models import Verifier
from user.views import check_authority
import datetime
import json
from django.utils.http import urlquote  # 传输中文到前端


def show_done(request):
    return render(request, 'done.html', {'msg_cn': '提交成功，感谢', 'msg_en': 'Submission successful, thank you'})


def show_error(request):
    return render(request, 'error.html', {'msg_cn': '验证码错误', 'msg_en': 'Incorrect verification code'})


def save_pax(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname').upper()
        flight = request.POST.get('flight').upper()
        flight_date = request.POST.get('flightDate')
        departure = request.POST.get('departure').upper()
        arrival = request.POST.get('arrival').upper()
        seat = request.POST.get('seat').upper()
        baggage = request.POST.get('baggage').upper()
        id_type = request.POST.get('idType')
        id_number = request.POST.get('idNumber')
        dialling_code = request.POST.get('diallingCode')
        telephone = request.POST.get('telephone')
        inbound_country = request.POST.get('inboundCountry').upper()
        inbound_flight = request.POST.get('inboundFlight').upper()
        inbound_date = request.POST.get('inboundDate')
        quarantine_end = request.POST.get('quarantineEnd')
        body_temperature = request.POST.get('bodyTemperature')
        healthy_code = request.POST.get('healthyCode')
        address = request.POST.get('address').upper()
        # code = request.POST.get('code')
        # flight = flight if len(flight) == 6 else flight[:2] + '0' + flight[2:]
        # verifier = Verifier.objects.filter(code=code)
        response = redirect('collect_pax')
        try:
            for n in request.COOKIES.keys():
                if n != 'csrftoken':
                    response.delete_cookie(n)
            cookie_dict = {n: c
                           for n, c in {'fullname': fullname, 'flight': flight, 'flight_date': flight_date,
                                        'departure': departure, 'arrival': arrival, 'id_type': id_type,
                                        'id_number': id_number, 'dialling_code': dialling_code, 'telephone': telephone,
                                        'inbound_country': inbound_country, 'inbound_flight': inbound_flight,
                                        'inbound_date': inbound_date, 'quarantine_end': quarantine_end,
                                        'body_temperature': body_temperature, 'healthy_code': healthy_code,
                                        'address': address, 'seat': seat, 'baggage': baggage}.items() if c != ''}
            for n, c in cookie_dict.items():
                response.set_cookie(n, urlquote(c), 7200)
        except:
            pass
        return response


def collect_pax(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname').upper()
        flight = request.POST.get('flight').upper()
        flight_date = request.POST.get('flightDate')
        departure = request.POST.get('departure').upper()
        arrival = request.POST.get('arrival').upper()
        seat = request.POST.get('seat').upper()
        baggage = request.POST.get('baggage').upper()
        id_type = request.POST.get('idType')
        id_number = request.POST.get('idNumber')
        dialling_code = request.POST.get('diallingCode')
        telephone = request.POST.get('telephone')
        inbound_country = request.POST.get('inboundCountry').upper()
        inbound_flight = request.POST.get('inboundFlight').upper()
        inbound_date = request.POST.get('inboundDate')
        quarantine_end = request.POST.get('quarantineEnd')
        body_temperature = request.POST.get('bodyTemperature')
        healthy_code = request.POST.get('healthyCode')
        address = request.POST.get('address').upper()
        valid, invalid_list = check_valudate(request, check_fullname_validate, check_flight_validate, check_flight_date_validate,
                              check_departure_validate, check_arrival_validate, check_seat_validate,
                              check_baggage_validate, check_id_type_validate, check_id_number_validate,
                              check_dialling_code_validate, check_telephone_validate, check_inbound_country_validate,
                              check_inbound_flight_validate, check_inbound_date_validate, check_quarantine_end_validate,
                              check_body_temperature_validate, check_healthy_code_validate)
        if not valid:
            response = render(request, 'pax.html',
                              {'msg_cn': '请按要求完善信息', 'msg_en': 'Please complete the form as required', 'invalid_list': invalid_list})
            cookie_dict = {n: c
                           for n, c in {'fullname': fullname, 'flight': flight, 'flight_date': flight_date,
                                        'departure': departure, 'arrival': arrival, 'id_type': id_type,
                                        'id_number': id_number, 'dialling_code': dialling_code, 'telephone': telephone,
                                        'inbound_country': inbound_country, 'inbound_flight': inbound_flight,
                                        'inbound_date': inbound_date, 'quarantine_end': quarantine_end,
                                        'body_temperature': body_temperature, 'healthy_code': healthy_code,
                                        'address': address, 'seat': seat, 'baggage': baggage}.items() if c != ''}
            for n in request.COOKIES.keys():
                if n != 'csrftoken':
                    response.delete_cookie(n)
            try:
                for n, c in cookie_dict.items():
                    response.set_cookie(n, urlquote(c), 7200)
            except:
                pass
            return response
        code = request.POST.get('code')
        flight = flight if len(flight) == 6 else flight[:2] + '0' + flight[2:]
        verifier = Verifier.objects.filter(code=code)
        if verifier.count() == 0:
            response = render(request, 'error.html', {'msg_cn': '验证码错误', 'msg_en': 'Incorrect verification code'})
            cookie_dict = {n: c
                           for n, c in {'fullname': fullname, 'flight': flight, 'flight_date': flight_date,
                                        'departure': departure, 'arrival': arrival, 'id_type': id_type,
                                        'id_number': id_number, 'dialling_code': dialling_code, 'telephone': telephone,
                                        'inbound_country': inbound_country, 'inbound_flight': inbound_flight,
                                        'inbound_date': inbound_date, 'quarantine_end': quarantine_end,
                                        'body_temperature': body_temperature, 'healthy_code': healthy_code,
                                        'address': address, 'seat': seat, 'baggage': baggage}.items() if c != ''}
            for n in request.COOKIES.keys():
                if n != 'csrftoken':
                    response.delete_cookie(n)
            try:
                for n, c in cookie_dict.items():
                    response.set_cookie(n, urlquote(c), 3600)
            except:
                pass
            return response
        if Passenger.objects.filter(flight=flight, flight_date=flight_date, id_number=id_number).count() > 0:
            return render(request, 'error.html', {'msg_cn': '您已经提交成功，请勿重复提交',
                                                 'msg_en': 'You have submitted successfully, Duplicate submissions are not allowed!'})
        # try:
        Passenger.objects.create(fullname=fullname, flight=flight, flight_date=flight_date, departure_city=departure,
                                 arrival_city=arrival, seat=seat, baggage=baggage, id_type=id_type, id_number=id_number,
                                 dialling_code=dialling_code, telephone=telephone, inbound_country=inbound_country,
                                 inbound_flight=inbound_flight, inbound_date=inbound_date,
                                 quarantine_end=quarantine_end, body_temperature=body_temperature,
                                 healthy_code=healthy_code, address=address, verifier=verifier[0])
        response = render(request, 'done.html', {'msg_cn': '提交成功，感谢', 'msg_en': 'Submission successful, thank you'})
        for n in request.COOKIES.keys():
            if n != 'csrftoken':
                response.delete_cookie(n)
        return response
        # except:
        #     return render(request, 'done.html', {'msg_cn': '提交失败，请联系工作人员',
        #                                          'msg_en': 'Submission failed, please contact staff'})
    else:
        return render(request, 'pax.html')


@check_authority
def export_pax(request):
    if request.method == 'POST':
        flight = request.POST.get('flight').upper()
        flight_date = request.POST.get('flightDate')
        flight = flight if len(flight) == 6 else flight[:2] + '0' + flight[2:]
        pax = Passenger.objects.filter(flight=flight, flight_date=flight_date)
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if pax.count() == 0:
            return JsonResponse('({}) {} {}\n无数据'.format(time, flight, flight_date), safe=False)
        pax = pax.values()
        text = '({}) {} {} 共{}条数据\n'.format(time, flight, flight_date, pax.count())
        for i, v in enumerate(pax):
            text += """序号:{}\n姓名:{}\n航班号:{}\n起飞时间:{}\n起飞地:{}\n目的地:{}\n座位号:{}\n托运行李件数:{}\n证件类别:{}\n证件号:{}\n联系电话区号:{}\n联系电话:{}\n入境地区:{}\n入境航班号:{}\n入境时间:{}\n解除隔离时间:{}\n体温状态:{}\n健康码:{}\n目的地详细地址:{}\n\n\n""".format(
                i+1, v['fullname'], v['flight'], v['flight_date'], v['departure_city'], v['arrival_city'], v['seat'],
                v['baggage'], v['id_type'], v['id_number'], v['dialling_code'], v['telephone'], v['inbound_country'],
                v['inbound_flight'], v['inbound_date'], v['quarantine_end'], v['body_temperature'], v['healthy_code'],
                v['address']
            )
        return JsonResponse(text, safe=False)
    else:
        return render(request, 'export_pax.html')


@check_authority
def show_flight_list(request):
    if request.method == 'POST':
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        flight_date = request.POST.get('flightDate')
        flight_list = list(set(list(Passenger.objects.filter(flight_date=flight_date).values_list('flight', flat=True))))
        flight_list.sort()
        text = '({}) {} 数量:{}'.format(time, flight_date, len(flight_list))
        flight_list.insert(0, text)
        return JsonResponse(flight_list, safe=False)
    else:
        return render(request, 'export_pax.html')


def upload_passenger_list(request):
    if request.method == 'POST':
        passenger_list = request.FILES.get('upload_passenger_list')

    else:
        return render(request, 'error_403.html', status=403)


def check_fullname_validate(request):
    if request.method == 'GET':
        fullname = request.GET.get('fullname')
    else:
        fullname = request.POST.get('fullname')
    if fullname == '':
        return HttpResponse('姓名不能为空 A name is required')
    if len(fullname) < 2:
        return HttpResponse('姓名格式不正确 Fullname is not valid')
    if not re.search(r'^[_a-zA-Z0-9\x20\u4e00-\u9fa5]+$', fullname):
        return HttpResponse('姓名格式不正确 Fullname is not valid')
    return HttpResponse('')


def check_flight_validate(request):
    if request.method == 'GET':
        flight = request.GET.get('flight')
    else:
        flight = request.POST.get('flight')
    if flight == '':
        return HttpResponse('航班号不能为空 A flight number is required')
    if len(flight) < 5 or len(flight) > 6:
        return HttpResponse('航班号格式不正确 Flight number is not valid')
    if not re.search(r'^\w{2}\d{3,4}$', flight):
        return HttpResponse('航班号格式不正确 Flight number is not valid')
    return HttpResponse('')


def check_flight_date_validate(request):
    if request.method == 'GET':
        flight_date = request.GET.get('flightDate')
    else:
        flight_date = request.POST.get('flightDate')
    if flight_date == '':
        return HttpResponse('航班日期不能为空 Flight date is required')
    return HttpResponse('')


def check_departure_validate(request):
    if request.method == 'GET':
        departure = request.GET.get('departure')
    else:
        departure = request.POST.get('departure')
    if departure == '':
        return HttpResponse('始发地不能为空 A departure city is required')
    if len(departure) < 2:
        return HttpResponse('始发地格式不正确 Departure city is not valid')
    if not re.search(r'^[_a-zA-Z0-9\x20\u4e00-\u9fa5]+$', departure):
        return HttpResponse('始发地格式不正确 Departure city is not valid')
    return HttpResponse('')


def check_arrival_validate(request):
    if request.method == 'GET':
        arrival = request.GET.get('arrival')
    else:
        arrival = request.POST.get('arrival')
    if arrival == '':
        return HttpResponse('目的地不能为空 An arrival city is required')
    if len(arrival) < 2:
        return HttpResponse('目的地格式不正确 Arrival city is not valid')
    if not re.search(r'^[_a-zA-Z0-9\x20\u4e00-\u9fa5]+$', arrival):
        return HttpResponse('目的地格式不正确 Arrival city is not valid')
    return HttpResponse('')


def check_seat_validate(request):
    if request.method == 'GET':
        seat = request.GET.get('seat')
    else:
        seat = request.POST.get('seat')
    if seat == '':
        return HttpResponse('座位号不能为空 A seat number city is required')
    if len(seat) < 2 or len(seat) > 3:
        return HttpResponse('座位号格式不正确 Seat number is not valid')
    if not re.search(r'^\d{1,2}\w$', seat):
        return HttpResponse('座位号格式不正确 Arrival city is not valid')
    return HttpResponse('')


def check_baggage_validate(request):
    if request.method == 'GET':
        baggage = request.GET.get('baggage')
    else:
        baggage = request.POST.get('baggage')
    if baggage == '':
        return HttpResponse('托运行李件数不能为空 Number of checked baggage is required')
    if not re.search(r'^\d{1,2}$', baggage):
        return HttpResponse('托运行李件数格式不正确 Number of checked baggage is not valid')
    if int(baggage) < 0 or int(baggage) > 50:
        return HttpResponse('托运行李件数不正确 Number of checked baggage is not valid')
    return HttpResponse('')


def check_id_type_validate(request):
    if request.method == 'GET':
        id_type = request.GET.get('idType')
    else:
        id_type = request.POST.get('idType')
    if id_type == '':
        return HttpResponse('证件类别不能为空 An id type is required')
    if len(id_type) < 2 or len(id_type) > 10:
        return HttpResponse('证件类别格式不正确 Id type is not valid')
    if not re.search(r'^[_a-zA-Z0-9\x20\u4e00-\u9fa5]+$', id_type):
        return HttpResponse('证件类别格式不正确 Id type is not valid')
    return HttpResponse('')


def check_id_number_validate(request):
    if request.method == 'GET':
        id_type = request.GET.get('idType')
        id_number = request.GET.get('idNumber')
    else:
        id_type = request.POST.get('idType')
        id_number = request.POST.get('idNumber')
    if id_type == '':
        return HttpResponse('请选择证件类别 An id type is required')
    if id_number == '':
        return HttpResponse('证件号不能为空 An id number city is required')
    if id_type == '身份证':
        if len(id_number) != 15 and len(id_number) != 18:
            return HttpResponse('证件号格式不正确 Id number is not valid')
        if not re.search(r'(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)', id_number):
            return HttpResponse('证件号格式不正确 Id number is not valid')
    if id_type == '护照':
        if len(id_number) < 5 or len(id_number) > 12:
            return HttpResponse('证件号格式不正确 Id number is not valid')
        if not re.search(r'^\w{5,12}$', id_number):
            return HttpResponse('证件号格式不正确 Id number is not valid')
    return HttpResponse('')


def check_dialling_code_validate(request):
    if request.method == 'GET':
        dialling_code = request.GET.get('diallingCode')
    else:
        dialling_code = request.POST.get('diallingCode')
    if dialling_code == '':
        return HttpResponse('电话区号不能为空 A dialling code city is required')
    if len(dialling_code) < 2 or len(dialling_code) > 5:
        return HttpResponse('电话区号格式不正确 Dialling code is not valid')
    if not re.search(r'^\d{2,5}$', dialling_code):
        return HttpResponse('电话区号格式不正确 Dialling code is not valid')
    return HttpResponse('')


def check_telephone_validate(request):
    if request.method == 'GET':
        telephone = request.GET.get('telephone')
    else:
        telephone = request.POST.get('telephone')
    if telephone == '':
        return HttpResponse('联系电话不能为空 A telephone number is required')
    if len(telephone) < 5 or len(telephone) > 20:
        return HttpResponse('联系电话格式不正确 Telephone number is not valid')
    if not re.search(r'^\d{5,20}$', telephone):
        return HttpResponse('联系电话格式不正确 Telephone number is not valid')
    return HttpResponse('')


def check_inbound_country_validate(request):
    if request.method == 'GET':
        inbound_country = request.GET.get('inboundCountry')
    else:
        inbound_country = request.POST.get('inboundCountry')
    if inbound_country == '':
        return HttpResponse('入境地区不能为空 An inbound region is required')
    if len(inbound_country) < 2 or len(inbound_country) > 30:
        return HttpResponse('入境地区格式不正确 Inbound region is not valid')
    if not re.search(r'^[a-zA-Z0-9\x20\u4e00-\u9fa5]+$', inbound_country):
        return HttpResponse('入境地区格式不正确 Inbound region is not valid')
    return HttpResponse('')


def check_inbound_flight_validate(request):
    if request.method == 'GET':
        inbound_flight = request.GET.get('inboundFlight')
    else:
        inbound_flight = request.POST.get('inboundFlight')
    if inbound_flight == '':
        return HttpResponse('入境航班号不能为空 An inbound flight number is required')
    if len(inbound_flight) < 5 or len(inbound_flight) > 6:
        return HttpResponse('入境航班号格式不正确 Inbound flight number is not valid')
    if not re.search(r'^\w{2}\d{3,4}$', inbound_flight):
        return HttpResponse('入境航班号格式不正确 Inbound flight number is not valid')
    return HttpResponse('')


def check_inbound_date_validate(request):
    if request.method == 'GET':
        inbound_date = request.GET.get('inboundDate')
    else:
        inbound_date = request.POST.get('inboundDate')
    if inbound_date == '':
        return HttpResponse('航班日期不能为空 Inbound date is required')
    return HttpResponse('')


def check_quarantine_end_validate(request):
    if request.method == 'GET':
        quarantine_end = request.GET.get('quarantineEnd')
    else:
        quarantine_end = request.POST.get('quarantineEnd')
    if quarantine_end == '':
        return HttpResponse('解除隔离日期不能为空 Date of lifting quarantine is required')
    return HttpResponse('')


def check_body_temperature_validate(request):
    if request.method == 'GET':
        body_temperature = request.GET.get('bodyTemperature')
    else:
        body_temperature = request.POST.get('bodyTemperature')
    if body_temperature == '':
        return HttpResponse('体温不能为空 A body temperature is required')
    if not re.search(r'^\d{2}\.?\d{0,2}?$', body_temperature):
        return HttpResponse('体温格式不正确 Body temperature is not valid')
    if float(body_temperature) < 30 or float(body_temperature) > 43:
        return HttpResponse('体温格式不正确 Body temperature is not valid')
    return HttpResponse('')


def check_healthy_code_validate(request):
    if request.method == 'GET':
        healthy_code = request.GET.get('healthyCode')
    else:
        healthy_code = request.POST.get('healthyCode')
    if healthy_code == '':
        return HttpResponse('健康码不能为空 A healthy code is required')
    if len(healthy_code) < 2 or len(healthy_code) > 10:
        return HttpResponse('健康码格式不正确 Healthy code is not valid')
    if not re.search(r'^[a-zA-Z0-9\x20\u4e00-\u9fa5]+$', healthy_code):
        return HttpResponse('健康码格式不正确 Healthy code is not valid')
    return HttpResponse('')


def check_address_validate(request):
    if request.method == 'GET':
        address = request.GET.get('address')
    else:
        address = request.POST.get('address')
    if address == '':
        return HttpResponse('目的地住址不能为空 A destination address is required')
    if len(address) < 10 or len(address) > 200:
        return HttpResponse('目的地住址格式不正确 Destination address is not valid')
    if not re.search(r'^[a-zA-Z0-9\x20\u4e00-\u9fa5]+$', address):
        return HttpResponse('目的地住址格式不正确 Destination address is not valid')
    return HttpResponse('')


def check_code_validate(request):
    if request.method == 'GET':
        code = request.GET.get('code')
    else:
        code = request.POST.get('code')
    if code == '':
        return HttpResponse('验证码不能为空 A verification code is required')
    if len(code) != 4:
        return HttpResponse('验证码格式不正确 Verification code is not valid')
    if not re.search(r'^\d{4}$', code):
        return HttpResponse('验证码格式不正确 Verification code is not valid')
    return HttpResponse('')


# def check_passwords_validate(request):
#     if request.method == 'GET':
#         params = request.GET.dict()
#     except MultiValueDictKeyError:
#         params = request.POST.dict()
#     for key, value in params.items():
#         if "password" in key:
#             if key == "":
#                 return HttpResponse('密码不能为空')
#             if len(key) < 6 or len(key) > 16:
#                 return HttpResponse('密码不能少于6个字符或超过16个字符')
#             if not re.search(r'^\S+$', key):
#                 return HttpResponse('密码包含非法字符(‘ ’)')
#     return HttpResponse('')


def check_valudate(request, *args):
    invalid_list = []
    check_method = args
    for method in check_method:
        if method(request).content != b'':
            invalid_list.append(method(request).content.decode())
    if len(invalid_list) != 0:
        return False, invalid_list
    return True, invalid_list

