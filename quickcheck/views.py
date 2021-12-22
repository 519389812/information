from django.shortcuts import render


def quickcheck(request):
    return render(request, 'quickcheck.html')
