from django.shortcuts import render


def mainbase(request):
    return render(request, template_name='main/base.html')
