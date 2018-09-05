from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.http import HttpResponseNotAllowed, JsonResponse
from .utils import cURL_AT_request, cURL_REV_request
from django.urls import reverse
import json
from django.core.mail import send_mail, BadHeaderError
import urllib
import time


client_id='a4KPlQ7SV2qjsSMF6TOKWvmZ36QEUI25E8Dvn6sL'
client_secret='heRhnOayEOLyh0cWR2C8RqPhrAhOR8Cmrgx4a5eMmht7sFY6bQcRIphsT9TUkL62yMjdJXL6t9sXn0ynxLGSrH0hPr1r1dKqOahncNJHcvRV2W4uTqnMZwzY61LPj8tI'

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

def online_data(request, language):
    '''if request.session._session:
        return render(request, 'webapp/online_data.html')
    else:
        return render(request, 'webapp/home.html')'''
    url = 'http://poseidonsystem.gr:8000/api/online_data_from_mv/'
    serialized_data = urllib.request.urlopen(url).read()

    finaldata ={
        'TS_MO_ATHOS':{
            15: 'N/A',
            19: 'N/A',
            33: 'N/A',
            22: 'N/A',
            32: 'N/A',
            112: 'N/A',
            14: 'N/A',
            122: 'N/A',
            27: 'N/A',
            24: 'N/A',
            23: 'N/A'
        },
        'TS_MO_MYKON':{
            15: 'N/A',
            19: 'N/A',
            33: 'N/A',
            22: 'N/A',
            32: 'N/A',
            112: 'N/A',
            14: 'N/A',
            122: 'N/A',
            27: 'N/A',
            24: 'N/A',
            23: 'N/A'
        },
        'TS_MO_SARON':{
             15: 'N/A',
            19: 'N/A',
            33: 'N/A',
            22: 'N/A',
            32: 'N/A',
            112: 'N/A',
            14: 'N/A',
            122: 'N/A',
            27: 'N/A',
            24: 'N/A',
            23: 'N/A'
        },
        'TS_MO_HERAKLION':{
             15: 'N/A',
            19: 'N/A',
            33: 'N/A',
            22: 'N/A',
            32: 'N/A',
            112: 'N/A',
            14: 'N/A',
            122: 'N/A',
            27: 'N/A',
            24: 'N/A',
            23: 'N/A'
        },
        'TS_MO_68422':{
             15: 'N/A',
            19: 'N/A',
            33: 'N/A',
            22: 'N/A',
            32: 'N/A',
            112: 'N/A',
            14: 'N/A',
            122: 'N/A',
            27: 'N/A',
            24: 'N/A',
            23: 'N/A'
        },
        'TS_MO_61277':{
             15: 'N/A',
            19: 'N/A',
            33: 'N/A',
            22: 'N/A',
            32: 'N/A',
            112: 'N/A',
            14: 'N/A',
            122: 'N/A',
            27: 'N/A',
            24: 'N/A',
            23: 'N/A'
        }
    }
    
    data = json.loads(serialized_data.decode('utf-8'))
    results = data['results']
    #date = dateutil.parser.parse(results[0]['dt'])
    date = time.strptime(results[0]['dt'], '%Y-%m-%dT%H:%M:%SZ')
    finaldate =time.strftime('%d.%m.%Y %H:%M', date)
    for row in results:
        finaldata[row['platform']][row['param']]=row['val']
    path =request.path.split('/')
    print(path[2])
    if path[2]=='online_data_table':
        return render(request, 'webapp/online_data_table.html', {'data' : finaldata, 'date': finaldate, 'lang':language})
    if path[2]=='online_data_poseidon':
        return render(request, 'webapp/online_data_poseidon.html', {'data' : finaldata, 'date': finaldate, 'lang':language})

def logout(request):
    if request.session._session:
        token=request.session['refresh_token']
        token_type='refresh_token'
        curl_res = cURL_REV_request(token, token_type, client_id, client_secret)
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
    curl_res = cURL_AT_request(code, redirect_url, client_id, client_secret)
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
    request.session[key] = new_value
    return HttpResponse('ok')


def get_session(request):
    if not request.is_ajax() or not request.method=='GET':
        return HttpResponse("Error")
    key=request.GET.get('key', '')
    value=request.session[key]
    return JsonResponse({'data':value}) 

#class CreateNetcdf(APIView)
def create_netcdf(request):
    print(request)
    #data=list(request.POST.keys())
    #data=dict(request.POST.lists())
    data=json.loads(request.POST.get('datas', None))
    print('here:', list(data.keys()))
    print('data', data['dt_from'])
    print(data['platforms']['TS'][0])
    return JsonResponse({'success': data})
