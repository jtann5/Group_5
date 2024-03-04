from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterForm, AuthForm, BuildingForm
from django.http import HttpResponseForbidden, HttpResponseRedirect
#from .models import UserAccount
from .models import *
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'home.html')

def support(request):
    return render(request, 'support.html')

@login_required(login_url="/login")
def dashboard(request):
    if request.user.is_superuser:
        return admin_dashboard(request)
    elif request.user.manager != None:
        return manager_dashboard(request)
    else:
        return tenant_dashboard(request)

@login_required(login_url="/login")
def admin_dashboard(request):
    users = UserAccount.objects.all()
    applications = HousingApplication.objects.all()
    requests = MaintenanceRequest.objects.all()
    buildings = Building.objects.all()
    per_page = 10
    paginator = Paginator(users, per_page)
    page = request.GET.get('page', 1)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    if request.user.is_superuser:
        return render(request, 'dashboard/admin_dashboard.html', {'users': users, 'applications': applications, 'requests': requests, 'buildings': buildings})
    else:
        return handler_403(request)

@login_required(login_url="/login")
def manager_dashboard(request):
    users = UserAccount.objects.all()
    applications = HousingApplication.objects.all()
    requests = MaintenanceRequest.objects.all()
    per_page = 10
    paginator = Paginator(users, per_page)
    page = request.GET.get('page', 1)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)

    if request.user.manager != None:
        return render(request, 'dashboard/tenant_dashboard.html', {'users':users, 'applications':applications, 'requests':requests})
    else:
        return handler_403(request)

@login_required(login_url="/login")
def tenant_dashboard(request):
    applications = HousingApplication.objects.all()
    requests = MaintenanceRequest.objects.filter(userId=request.user.id)

    return render(request, 'dashboard/tenant_dashboard.html', {'applications':applications, 'requests':requests})


@login_required(login_url="/login")
def application(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        unit = request.POST.get('unit')
        phone = request.POST.get('phone')
        application = HousingApplication.objects.create(first_name=first_name, last_name=last_name, unit_wanted=unit, phone=phone)
        UserHousingApplication.objects.create(userId = request.user, housingApplicationId=application)
        return redirect('/dashboard')
    return render(request, 'forms/application/application.html')

@login_required(login_url="/login")
def maintenance(request):
    buildings = Building.objects.all()
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        unit = request.POST.get('unit')
        req = request.POST.get('request')
        phone = request.POST.get('phone')
        building_id = request.POST.get('building')
        building = Building.objects.get(id=building_id)
        entry_permission = request.POST.get('entry_permission') == '1'
        MaintenanceRequest.objects.create(userId=request.user, first_name=first_name, last_name=last_name, address=address, unit=unit, request=req, phone=phone, building=building, entry_permission=entry_permission)
        return redirect('/dashboard')
    return render(request, 'forms/maintenance/maintenance.html', {'buildings': buildings})

def payment(request):
    return render(request, 'payment.html')

@login_required(login_url="/login")
def user_profile(request, username):
    return render(request, 'profile.html', {'user_profile' : username})

@login_required(login_url="/login")
def building_info(request, building_id):
    if request.user.is_superuser or request.user.manager != None:
        building = get_object_or_404(Building, pk=building_id)
        maintenance_requests = MaintenanceRequest.objects.filter(building=building)
        return render(request, 'dashboard/data/building_info.html', {'building': building, 'maintenance_requests': maintenance_requests})
    else:
        return handler_403(request)

@login_required(login_url="/login")
def request_info(request, request_id):
    maintenance_request = get_object_or_404(MaintenanceRequest, pk=request_id)
    if request.user.is_superuser or request.user.manager != None or request.user == maintenance_request.userId:
        return render(request, 'dashboard/data/request_info.html', {'maintenance_request': maintenance_request})
    else:
        return handler_403(request)

def mark_completed(request, request_id):
    maintenance_request = get_object_or_404(MaintenanceRequest, pk=request_id)
    notes = request.POST.get('notes')
    if request.method == 'POST' and request.user.is_superuser or request.user.manager != None:
        maintenance_request.completed = True
        maintenance_request.notes = notes
        maintenance_request.save()
        return redirect('request_info', request_id=request_id)
    else:
        return handler_403(request)


# Views for user accounts and authentication
def signup_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    else:
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                request.session.set_expiry(1800) # Set session expiry to 30 minutes
                return redirect('/')
        else:
            form = RegisterForm()
        
        return render(request, 'registration/signup.html', {"form": form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard')
    else:
        if request.method == 'POST':
            form = AuthForm(request.POST)
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                request.session.set_expiry(1800) # Set session expiry to 30 minutes
                next_url = request.GET.get('next', None)
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect('/dashboard')
        else:
            form = AuthForm(request)
        return render(request, 'registration/login.html', {"form": form})

def logout_view(request):
    logout(request)
    return redirect('/')

@login_required(login_url="/login")
def profile(request):
    return render(request, 'profile.html')

@login_required(login_url="/login")
def delete_user(request):
    user_id = request.GET.get('user_id', None)
    user_to_delete = UserAccount.objects.get(pk=user_id)
    if user_to_delete == None:
        return redirect('/')
    elif user_to_delete.id == request.user.id:
        logout(request)
        user_to_delete.delete()
        return redirect('/')
    elif request.user.is_superuser:
        user_to_delete.delete()
        return redirect('/dashboard')
    return redirect('/')

# Views for errors
def handler_404(request, exception):
    return render(request, 'errors/404.html', status=404)

def handler_403(request, exception=None):
    return render(request, 'errors/403.html', status=403)

@login_required(login_url="/login")
def add_building(request):
    user = request.user
    if user.is_superuser:
        form = BuildingForm()
        if request.method == 'POST':
            form = BuildingForm(request.POST)
            if form.is_valid():
                form.save()
                return dashboard(request)
        return render(request, 'dashboard/forms/create_building.html', {'form': form})
    else:
        return handler_403(request)