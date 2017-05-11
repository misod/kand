from django.shortcuts import render

def index(request) :
    return render(request, 'personal/home.html')

def contact(request):
    return render(request, 'personal/basic.html',{'content' :['If you would like to contact the developers, pleas email to','logflar@gmail.com']})

def information(request):
    return render(request, 'personal/basic.html',{'content' :['This site is under development but it will be a log system for gliders when it is done','If you would like to contact the developers, email to','conrad.aslund@gmail.com']})

def flylogs(request):
    return render(request, 'personal/basic.html',{'content' :['This site is under development but this will be the main button for logs']})


def signup(request):
    return render(request, 'personal/basic.html',{'content' :['If you would like to sign up and be abel to download the tabel in xlsx or csv, email to conrad.aslund@gmail.com']})
# Create your views here.
