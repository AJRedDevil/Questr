from django.shortcuts import render

def index(request):
    nextlink = "login"
    return render(request, 'index.html', locals())

def loadPage(request, template):
    return render(request, template, locals())   