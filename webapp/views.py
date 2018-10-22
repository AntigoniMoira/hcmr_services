"""
Views for webapp.
"""
import urllib
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
)


def home(request):
    """
    Return home.html page.
    """
    if request.session._session:
        response = HttpResponseRedirect('/webapp/index/')
        return response
    else:
        return render(request, 'webapp/home.html')


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
    redirect_url = 'http://localhost:9000/webapp/access_token/'
    curl_res = cURL_AT_request(code, redirect_url)
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
    url = 'http://localhost:8000/auth/user_details/'
    token = request.session['access_token']
    curl_res = cURL_GET_request(token, url)
    request.session['email'] = json.loads(curl_res.text)['email']
    return HttpResponseRedirect('../poseidon_db/')


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
            url = 'http://localhost:8000/auth/user_details/'
            token = request.session['access_token']
            curl_res = cURL_GET_request(token, url)
            if curl_res.status_code == 401:
                token = update_access_token(request)
                curl_res = cURL_GET_request(token, url)
            data = json.loads(curl_res.text)
            return render(request, 'webapp/user_profile.html', {'data': data})
        if request.method == 'POST':
            data = json.loads(request.POST.get('data', None))
            url = 'http://localhost:8000/auth/user_details/'
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
            url = 'http://localhost:8000/auth/new_password/'
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
        url = 'http://localhost:8000/auth/activate/'
        token = request.session['access_token']
        curl_res = cURL_GET_request(token, url)
        if curl_res.status_code == 401:
            token = update_access_token(request)
            curl_res = cURL_GET_request(token, url)
        users = json.loads(curl_res.text)['data']
        return render(request, 'webapp/activate_users.html', {'users': users})
    if request.method == 'POST':
        data = {
            'email': request.POST.get('email', None)
        }
        url = 'http://localhost:8000/auth/activate/'
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
        url = 'http://localhost:8000/auth/delete_user/'
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
    url = 'http://localhost:8001/api/online_data_from_mv/'
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

    data = json.loads(serialized_data)
    results = data['results']
    #date = dateutil.parser.parse(results[0]['dt'])
    date = time.strptime(results[0]['dt'], '%Y-%m-%dT%H:%M:%SZ')
    finaldate = time.strftime('%d.%m.%Y %H:%M', date)
    for row in results:
        finaldata[row['platform']][row['param']] = row['val']
    path = request.path.split('/')
    if path[2] == 'online_data_table':
        return render(request, 'webapp/online_data_table.html', {'data': finaldata, 'date': finaldate, 'lang': language})
    if path[2] == 'online_data_poseidon':
        return render(request, 'webapp/online_data_poseidon.html', {'data': finaldata, 'date': finaldate, 'lang': language})


def poseidon_db(request):
    """
    View to return poseidon_db.html.
    """
    if request.session._session:
        return render(request, 'webapp/poseidon_db.html')
    else:
        response = HttpResponseRedirect('/webapp/home/')
        return response


def platforms_between(request):
    """
    View to return platforms with measurements between a start date and an end data.
    """
    if request.method == 'GET':
        url = 'http://localhost:8001/api/poseidon_platforms_with_measurements_between/?start_date=' + \
            request.GET.get('start_date', None)+'&end_date=' + \
            request.GET.get('end_date', None)
        token = request.session['access_token']
        curl_res = cURL_GET_request(token, url)
        if curl_res.status_code == 401:
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
        url = 'http://localhost:8001/api/poseidon_platform_parameters_with_measurements_between/?platform=' + \
            request.GET.get('platform', None)+'&start_date=' + request.GET.get(
                'start_date', None)+'&end_date='+request.GET.get('end_date', None)
        token = request.session['access_token']
        curl_res = cURL_GET_request(token, url)
        if curl_res.status_code == 401:
            token = update_access_token(request)
            curl_res = cURL_GET_request(token, url)
        return JsonResponse({
            'data': json.loads(curl_res.text)['data']
        })
    if request.method == 'POST':
        response = HttpResponseRedirect('/webapp/error/')
        return response

def create_netcdf(request):
    print(request)
    # data=list(request.POST.keys())
    # data=dict(request.POST.lists())
    data = json.loads(request.POST.get('datas', None))
    #print('here:', list(data.keys()))
    print('data', data['dt_from'])
    # print(data['platforms']['TS'][0])
    print(data['user_email'])
    return JsonResponse({'success': data})
