from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.http import HttpResponseNotAllowed, JsonResponse
from .utils import cURL_request
import json


def index(request):
    '''if not request.user.is_authenticated:
         return redirect('/webapp/login/')
    else:'''
    #print(request.session['access_token'])
    #print(request.session['refresh_token'])
    return render(request, 'webapp/index.html')

def help(request):
    return render(request, 'webapp/help.html')

def poseidon_db(request):
    return render(request, 'webapp/poseidon_db.html')

def online_data(request):
    return render(request, 'webapp/online_data.html')

def login(request):
     return render(request, 'webapp/login.html')

def home(request):
     return render(request, 'webapp/home.html')

def access_token(request):
    code=request.GET.get('code')
    redirect_url='http://localhost:9000/webapp/access_token/'
    cliend_id='a4KPlQ7SV2qjsSMF6TOKWvmZ36QEUI25E8Dvn6sL'
    cliend_secret='heRhnOayEOLyh0cWR2C8RqPhrAhOR8Cmrgx4a5eMmht7sFY6bQcRIphsT9TUkL62yMjdJXL6t9sXn0ynxLGSrH0hPr1r1dKqOahncNJHcvRV2W4uTqnMZwzY61LPj8tI'
    curl_res = cURL_request(code, redirect_url, cliend_id, cliend_secret)
    access_token=json.loads(curl_res.text)['access_token']
    request.session['access_token']=access_token
    request.session['refresh_token']=json.loads(curl_res.text)['refresh_token']
    return HttpResponseRedirect('../index')

def update_session(request):
    if not request.is_ajax() or not request.method=='POST':
        return HttpResponseNotAllowed(['POST'])

    key=request.POST.get('key', '')
    new_value=request.POST.get('value', '')
    request.session[key] = value
    return HttpResponse('ok')


def get_session(request):
    if not request.is_ajax() or not request.method=='GET':
        return HttpResponse("Error")
    key=request.GET.get('key', '')
    value=request.session[key]
    return JsonResponse({'data':value}) 