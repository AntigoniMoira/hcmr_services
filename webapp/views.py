from django.shortcuts import render, redirect


def index(request):
    '''if not request.user.is_authenticated:
         return redirect('/webapp/login/')
    else:'''
    return render(request, 'webapp/index.html')

def help(request):
    return render(request, 'webapp/help.html')

def poseidon_db(request):
    return render(request, 'webapp/poseidon_db.html')

def online_data(request):
    return render(request, 'webapp/online_data.html')