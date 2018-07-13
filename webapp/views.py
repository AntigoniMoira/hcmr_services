from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.http import HttpResponseNotAllowed, JsonResponse
from .utils import cURL_AT_request, cURL_REV_request
from django.urls import reverse
import json
from django.core.mail import send_mail, BadHeaderError


def index(request):
    if request.session._session:
        return render(request, 'webapp/index.html')
    else:
        return render(request, 'webapp/home.html')

def error(request):
    if request.session._session:
        return render(request, 'webapp/error_page.html')
    else:
        return render(request, 'webapp/home.html')

def poseidon_db(request):
    if request.session._session:
        return render(request, 'webapp/poseidon_db.html')
    else:
        return render(request, 'webapp/home.html')

def online_data(request):
    '''if request.session._session:
        return render(request, 'webapp/online_data.html')
    else:
        return render(request, 'webapp/home.html')'''
    return render(request, 'webapp/online_data.html')

def logout(request):
    if request.session._session:
        token=request.session['refresh_token']
        token_type='refresh_token'
        curl_res = cURL_REV_request(token, token_type, cliend_id, cliend_secret)
        print(curl_res.status_code)
        if curl_res.status_code == 200:
            request.session.flush()
            return JsonResponse({
                    'success': True,
                    'redirectUri': reverse('home')
                })
        else:
            return JsonResponse({
                'success':False
            })
    else:
        return render(request, 'webapp/home.html')

def home(request):
    if request.session._session:
        return render(request, 'webapp/index.html')
    else:
        return render(request, 'webapp/home.html')

def access_token(request):
    code=request.GET.get('code')
    redirect_url='http://localhost:9000/webapp/access_token/'
    curl_res = cURL_AT_request(code, redirect_url, cliend_id, cliend_secret)
    print(json.loads(curl_res.text))
    access_token=json.loads(curl_res.text)['access_token']
    request.session['access_token']=access_token
    request.session['refresh_token']=json.loads(curl_res.text)['refresh_token']
    return HttpResponseRedirect('../index')

#Gia na mporei h js na pairnei ta dedomena pou einai apothikeymena sto session
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