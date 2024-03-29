from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import JsonResponse
from .models import Data
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
# Create your views here.
from django.core.cache import cache

def signup(request):
    if request.session.has_key('username'):
        username = request.session['username']
        if request.session.has_key('password'):
            password = request.session['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                return redirect('/display')
    elif request.method == 'POST':
        first_name = request.POST["first_name"]
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        print(request.POST)

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, ' username already exists')
                return redirect('signup')
            elif User.objects.filter(email=email).exists():
                messages.info(request, ' email ID already exists')
                return redirect('signup')
            elif first_name == '':
                messages.info(request, ' First Name field required')
            elif username == '':
                messages.info(request, ' Username field required')
            elif password1 == '':
                messages.info(request, ' Password field required')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email,
                                                first_name=first_name, last_name=last_name)
                user.save()
                return redirect('login')
        else:
            messages.info(request, 'password mismatch')
    return render(request, 'signup.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login(request):
    if request.session.has_key('username'):
        username = request.session['username']
        if request.session.has_key('password'):
            password = request.session['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('/display')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            request.session['username'] = username
            request.session['password'] = password
            return JsonResponse(
                {'success':True},
                safe=False
            )
        else:
            auth.login
            return JsonResponse(
                {'success':False},
                safe=False
            )
    else:
        return render(request, "login.html")
    return render(request, "login.html")

@login_required(login_url='/login')
def home(request):
    return render(request, 'login.html')


@login_required(login_url='/login')
def adddonor(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        phone = request.POST['phone']
        address = request.POST['address']
        bloodgroup = request.POST['bloodgroup']
        data = Data.objects.create(name=first_name, phone=phone, address=address, bloodgroup=bloodgroup)
        data.save()
        return redirect('/display')
    else:
        return render(request, 'register.html')

@login_required(login_url='/login')
def display(request):
    detail = Data.objects.all()
    return render(request, 'data.html', {'details': detail})

@login_required(login_url='/login')
def logout(request):
    try:
        auth.logout(request)
        request.session.flush()
        request.session.modified = True
    except:
        pass
    auth.logout(request)
    return redirect('/')
