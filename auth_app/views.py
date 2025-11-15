
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm

from django.contrib.auth.models import User



from .models import Address, Company, Profile


def home(request):
    return render(request, 'auth_app/home.html')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Save USER
            user = form.save()

            # Save Address
            address = Address.objects.create(
                street=form.cleaned_data['street'],
                suite=form.cleaned_data['suite'],
                city=form.cleaned_data['city'],
                zipcode=form.cleaned_data['zipcode']
            )

            # Save Company
            company = Company.objects.create(
                name=form.cleaned_data['company_name'],
                catchPhrase=form.cleaned_data['company_catchPhrase'],
                bs=form.cleaned_data['company_bs']
            )

            # Save Profile
            Profile.objects.create(
                user=user,
                phone=form.cleaned_data['phone'],
                website=form.cleaned_data['website'],
                address=address,
                company=company
            )

            return redirect('login')

    else:
        form = RegisterForm()

    return render(request, 'auth_app/register.html', {'form': form})

def login_view(request):
    error = None

    if request.method == 'POST':
        identifier = request.POST.get('username') 
        password = request.POST.get('password')

        
        try:
            user_obj = User.objects.get(email=identifier)
            username = user_obj.username
        except User.DoesNotExist:
            username = identifier  

       
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('/')
        else:
            error = "Invalid username/email or password."

    return render(request, 'auth_app/login.html', {'error': error})

def logout_view(request):
    logout(request)
    return redirect('login')



@login_required
def profile_view(request):
    return render(request, "auth_app/profile.html")
