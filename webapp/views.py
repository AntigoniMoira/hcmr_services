"""
Views for webapp.
"""
import urllib
import urllib.request
import time
import json
from django.shortcuts import render, HttpResponseRedirect
from django.http import JsonResponse
from .utils import (
    update_access_token,
    cURL_AT_request,
    cURL_REV_request,
    cURL_GET_request,
    cURL_POST_request,
    cURL_PUT_request,
    cURL_DELETE_request,
    get_tilte,
    get_params,
)

from django.conf import settings
from datetime import datetime


def home(request):
    """
    Return home.html page.
    """
    if request.session._session:
        response = HttpResponseRedirect('/webapp/index/')
        return response
    else:
        return render(request, 'webapp/home.html')


def index(request):
    """
    Return home.html page.
    """
    if request.session._session:
        return render(request, 'webapp/index.html')
    else:
        response = HttpResponseRedirect('/webapp/home/')
        return response


def gliders(request):
    """
    Return gliders.html page.
    """
    if request.session._session:
        return render(request, 'webapp/gliders.html')
    else:
        response = HttpResponseRedirect('/webapp/home/')
        return response


def weather_forecast(request):
    """
    Return gliders.html page.
    """
    product = request.GET.get('product_id', None)
    region = request.GET.get('area_id', None)

    if product == 'weather':
        file_path = 'meteo/fordates.METEO'
    elif product == 'sea-state':
        file_path = 'waves/fordates.WW3'
    elif product == 'sailing':
        file_path = 'waves/fordates.WW3'
    elif product == 'sea-level':
        file_path = 'surge/fordates.SL'
    elif product == 'ocean':
        file_path = 'ocean/fordates.PAEG'
    else: #ecosystem
        file_path = 'ecology/fordates.ERSEM_POM'


    if product == 'ecosystem' :
        with urllib.request.urlopen("http://poseidon.hcmr.gr/images/"+file_path) as url:
            s = url.read().decode().splitlines()
            dates = []
            now = datetime.utcnow()
            for line in s:
                value = line
                compdate = datetime(
                    int('20'+line[6:8]), int(line[3:5]), int(line[0:2]), int(line[14:16]))
                if compdate >= now:
                    dates.append({'html': compdate.strftime(
                        "%A") + ', ' + line, 'value': value})
    else:
        with urllib.request.urlopen("http://poseidon.hcmr.gr/images/"+file_path) as url:
            s = url.read().decode().splitlines()
            dates = []
            now = datetime.utcnow()
            modeldate = '/20'+s[0][6:8]+'/'+s[0][3:5]+'/'+s[0][0:2]+'/'
            for line in s:
                value = line[6:8]+line[3:5]+line[0:2]+line[14:16]
                compdate = datetime(
                    int('20'+line[6:8]), int(line[3:5]), int(line[0:2]), int(line[14:16]))
                if compdate >= now:
                    dates.append({'html': compdate.strftime(
                        "%A") + ', ' + line, 'value': value})
    title = get_tilte(product, region)
    params = get_params(product, region)
    return render(request, 'webapp/weather_forecast.html', {'dates': dates, 'region': region, 'modeldate': modeldate, 'title': title, 'params': params})


def error(request):
    """
    Return error.html page.
    """
    if request.session._session:
        return render(request, 'webapp/error_page.html')
    else:
        response = HttpResponseRedirect('/webapp/home/')
        return response


def access_token(request):
    """
    Exchange code with access and refresh token.
    """
    code = request.GET.get('code')
    state = request.GET.get('state', None)
    print(code)
    curl_res = cURL_AT_request(code)
    print(curl_res.text)
    request.session.set_expiry(60 * 60 * 24 * 7)
    request.session['access_token'] = json.loads(curl_res.text)['access_token']
    request.session['refresh_token'] = json.loads(curl_res.text)[
        'refresh_token']
    scope = json.loads(curl_res.text)['scope']
    if 'admin' in scope:
        request.session['scope'] = 'admin'
    elif 'staff' in scope:
        request.session['scope'] = 'staff'
    else:
        request.session['scope'] = 'user'
    url = settings.AUTH_DOMAIN + '/auth/user_details'
    token = request.session['access_token']
    curl_res = cURL_GET_request(token, url)
    request.session['email'] = json.loads(curl_res.text)['email']
    return HttpResponseRedirect('../' + state + '/')


def logout(request):
    """
    Logout user by terminate the session and revoke refresh token.
    """
    if request.session._session:
        token = request.session['refresh_token']
        token_type = 'refresh_token'
        curl_res = cURL_REV_request(token, token_type)
        if curl_res.status_code == 200:
            request.session.flush()
            response = HttpResponseRedirect('/webapp/home/')
        else:
            response = HttpResponseRedirect('/webapp/error/')
    else:
        response = HttpResponseRedirect('/webapp/home/')
    return response


def user_profile(request):
    """
    View to return user_profile.html or update user's profile.
    """
    if request.session._session:
        if request.method == 'GET':
            url = settings.AUTH_DOMAIN + '/auth/user_details/'
            token = request.session['access_token']
            curl_res = cURL_GET_request(token, url)
            if curl_res.status_code == 401:
                token = update_access_token(request)
                curl_res = cURL_GET_request(token, url)
            data = json.loads(curl_res.text)
            return render(request, 'webapp/user_profile.html', {'data': data})
        if request.method == 'POST':
            data = json.loads(request.POST.get('data', None))
            url = settings.AUTH_DOMAIN + '/auth/user_details/'
            token = request.session['access_token']
            curl_res = cURL_PUT_request(token, url, data)
            if curl_res.status_code == 401:
                token = update_access_token(request)
                curl_res = cURL_PUT_request(token, url, data)
            print(json.loads(curl_res.text))
            return JsonResponse({
                'success': json.loads(curl_res.text)['success']
            })
    else:
        response = HttpResponseRedirect('/webapp/home/')
        return response


def change_password(request):
    """
    view to update user's password.
    """
    if request.session._session:
        if request.method == 'POST':
            data = {
                'email': request.POST.get('email', None),
                'old_psw': request.POST.get('old_psw', None),
                'new_psw': request.POST.get('new_psw', None)
            }
            url = settings.AUTH_DOMAIN + '/auth/new_password/'
            token = request.session['access_token']
            curl_res = cURL_PUT_request(token, url, data)
            if curl_res.status_code == 401:
                token = update_access_token(request)
                curl_res = cURL_PUT_request(token, url, data)
            return JsonResponse({
                'success': json.loads(curl_res.text)['success'],
                'message': json.loads(curl_res.text)['message']
            })
    else:
        response = HttpResponseRedirect('/webapp/home/')
        return response


def activate_user(request):
    """
    View to return activate_users.html or update user's account (is_active=False -> is_active=True).
    """
    if request.method == 'GET':
        url = settings.AUTH_DOMAIN + '/auth/activate/'
        token = request.session['access_token']
        curl_res = cURL_GET_request(token, url)
        if curl_res.status_code == 401:
            token = update_access_token(request)
            curl_res = cURL_GET_request(token, url)
        inactive_users = json.loads(curl_res.text)['inactive']
        active_users = json.loads(curl_res.text)['active']
        return render(request, 'webapp/activate_users.html', {'inactive_users': inactive_users, 'active_users': active_users})
    if request.method == 'POST':
        data = {
            'email': request.POST.get('email', None)
        }
        url = settings.AUTH_DOMAIN + '/auth/activate/'
        token = request.session['access_token']
        curl_res = cURL_PUT_request(token, url, data)
        if curl_res.status_code == 401:
            token = update_access_token(request)
            curl_res = cURL_PUT_request(token, url, data)
        return JsonResponse({
            'success': json.loads(curl_res.text)['success']
        })


def delete_user(request):
    """
    View to delete a user from DB.
    """
    if request.method == 'POST':
        data = {
            'email': request.POST.get('email', None),
            'reason': request.POST.get('reason', None)
        }
        url = settings.AUTH_DOMAIN + '/auth/delete_user/'
        token = request.session['access_token']
        curl_res = cURL_DELETE_request(token, url, data)
        if curl_res.status_code == 401:
            token = update_access_token(request)
            curl_res = cURL_DELETE_request(token, url, data)
        return JsonResponse({
            'success': json.loads(curl_res.text)['success']
        })
    if request.method == 'GET':
        response = HttpResponseRedirect('/webapp/error/')
        return response


def online_data(request, language):
    """
    View to return online_data_poseidon.html or online_data_table.html page.
    """
    url = settings.API_DOMAIN + '/api/online_data_from_mv/'
    serialized_data = urllib.request.urlopen(url).read()

    finaldata = {
        'TS_MO_ATHOS': {
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
        'TS_MO_MYKON': {
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
        'TS_MO_SARON': {
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
        'TS_MO_HERAKLION': {
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
        'TS_MO_68422': {
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
        'TS_MO_61277': {
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
    # date = dateutil.parser.parse(results[0]['dt'])
    date = time.strptime(results[0]['dt'], '%Y-%m-%dT%H:%M:%SZ')
    finaldate = time.strftime('%d.%m.%Y %H:%M', date)
    for row in results:
        finaldata[row['platform']][row['param']] = row['val']
    path = request.path.split('/')
    if path[2] == 'online_data_table':
        if request.session._session:
            return render(request, 'webapp/online_data_table.html', {'data': finaldata, 'date': finaldate, 'lang': language})
        else:
            response = HttpResponseRedirect('/webapp/home/')
        return response
    if path[2] == 'online_data_poseidon':
        return render(request, 'webapp/online_data_poseidon.html', {'data': finaldata, 'date': finaldate, 'lang': language})


def online_data_map(request):
    """
    View to return online_data_map.html.
    """
    if request.session._session:
        return render(request, 'webapp/online_data_map.html')
    else:
        response = HttpResponseRedirect('/webapp/home/')
        return response


def poseidon_db(request):
    """
    View to return poseidon_db.html.
    """
    if request.session._session:
        return render(request, 'webapp/poseidon_db.html')
    else:
        url = 'http://localhost:8000/o/authorize/?response_type=code&state=poseidon_db&client_id=NwVaE1ddbUDyzlCf0MvdVy7fRbwGCskjXtMPJy0z&URI=/webapp/access_token/'
        response = HttpResponseRedirect(url)
        return response


def platforms_between(request):
    """
    View to return platforms with measurements between a start date and an end data.
    """
    if request.method == 'GET':
        url = settings.API_DOMAIN + '/api/poseidon_platforms_with_measurements_between/?start_date=' + \
            request.GET.get('start_date', None)+'&end_date=' + \
            request.GET.get('end_date', None)
        token = request.session['access_token']
        curl_res = cURL_GET_request(token, url)
        if curl_res.status_code == 403:
            token = update_access_token(request)
            curl_res = cURL_GET_request(token, url)
        return JsonResponse({
            'data': json.loads(curl_res.text)['data']
        })
    if request.method == 'POST':
        response = HttpResponseRedirect('/webapp/error/')
        return response


def measurements_between(request):
    """
    View to return platform's parameters with measurements between a start date and an end data.
    """
    if request.method == 'GET':
        url = settings.API_DOMAIN + '/api/poseidon_platform_parameters_with_measurements_between/?platform=' + \
            request.GET.get('platform', None)+'&start_date=' + request.GET.get(
                'start_date', None)+'&end_date='+request.GET.get('end_date', None)
        token = request.session['access_token']
        curl_res = cURL_GET_request(token, url)
        if curl_res.status_code == 403:
            token = update_access_token(request)
            curl_res = cURL_GET_request(token, url)
        return JsonResponse({
            'data': json.loads(curl_res.text)['data']
        })
    if request.method == 'POST':
        response = HttpResponseRedirect('/webapp/error/')
        return response


def create_netcdf(request):
    from subprocess import call
    data = json.loads(request.POST.get('data', None))
    req1 = json.dumps(data)
    print(req1)
    #response = call(["ssh", "user@10.6.1.16", "/home/user/scitools/bin/python ", "/home/user/scripts/api_script_tests/exe/create_poseidon_netcdf_htmlMail.py '%s'"%(req1)])
    # return JsonResponse({'success': response})
    return JsonResponse({'success': True})
