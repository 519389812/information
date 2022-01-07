from django.shortcuts import render, redirect, reverse
from user_agents import parse
from user.models import CustomUser
from django.contrib.auth.hashers import check_password
from django.contrib.auth import login as login_admin
from django.contrib.auth import logout as logout_admin
from django.contrib.auth import authenticate
from django.http import JsonResponse


def check_authority(func):
    def wrapper(*args, **kwargs):
        if not args[0].user.is_authenticated:
            if "X-Requested_With" in args[0].headers:
                return JsonResponse('请先登录', safe=False)
            return redirect('/login/?next=%s' % args[0].path)
        return func(*args, **kwargs)
    return wrapper


def check_is_touch_capable(func):
    def wrapper(*args, **kwargs):
        user_agent = parse(args[0].META.get('HTTP_USER_AGENT'))
        if not user_agent.is_touch_capable:
            if args[0].META.get('HTTP_REFERER'):
                return redirect(args[0].META.get('HTTP_REFERER')+'请使用触屏设备签名')
            else:
                return redirect('/')
        return func(*args, **kwargs)
    return wrapper


def check_post_validate(request, *args):
    check_method = args
    for method in check_method:
        if method(request).content != b'':
            return False
    return True


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login_admin(request, user)
            next_url = request.GET.get('next', '')
            if next_url != '':
                return redirect(next_url)
            else:
                return redirect('/')
        else:
            try:
                user = CustomUser.objects.get(username=username)
                if check_password(password, user.password):
                    if user.is_active:
                        return render(request, 'login.html', {'msg': '登录出错，请管理员！'})
                    else:
                        return render(request, 'login.html', {'msg': '用户未认证，请联系管理员审核！'})
                else:
                    return render(request, 'login.html', {'msg': '用户名或密码错误！'})
            except:
                return render(request, 'login.html', {'msg': '用户名或密码错误！'})
    else:
        if request.user.is_authenticated:
            return redirect('/')
        else:
            next_url = request.GET.get('next', '')
            return render(request, 'login.html', {'next': next_url})


def logout(request):
    logout_admin(request)
    return redirect(reverse('home'))
