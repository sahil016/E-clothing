from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from .models import *
from django.contrib.auth import authenticate, login as auth_login
from django.views.decorators.csrf import csrf_protect


def home(request):
    return render(request, 'dashboard.html')

from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from .models import User, Chairman, Member, Watchman

@csrf_protect 
def register(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            role = request.POST.get('role')
            phone = request.POST.get('phone')

            if User.objects.filter(phone=phone).exists():
                messages.error(request, "This phone number is already registered.")
                return redirect("register")

            # ✅ Create user properly
            user = User.objects.create_user(
                email=email,
                username=username,
                password=password,
                role=role,
                phone=phone
            )

            # ✅ Assign role-based models
            if role == 'chairman':
                Chairman.objects.create(user=user, start_date=request.POST.get('start_date'))
            elif role == 'member':
                Member.objects.create(user=user, house_no=request.POST.get('house_no'))
            elif role == 'watchman':
                Watchman.objects.create(user=user, shift=request.POST.get('shift', 'day'))

            messages.success(request, 'User registered successfully!')
            auth_login(request, user)  # ✅ Auto-login after registration
            return redirect('index')

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    return render(request, 'register.html')

    
@csrf_protect
def User_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            authenticated_user = authenticate(request, username=email, password=password)

            if authenticated_user:
                auth_login(request, authenticated_user)  
                request.session['email'] = authenticated_user.email
                request.session['is_active'] = authenticated_user.is_active  
                messages.success(request, "Login successful!")
                return redirect('member')  
            else:
                messages.error(request, "Invalid email or password")

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            msg = e

    return render(request, 'login.html',{'e':e})



@login_required
def custom_logout(request):
    user = request.user
    user.is_active = False  # Deactivate the user
    user.save()
    logout(request)
    return redirect('login')  # Redirect to login page or homepage

def profile(request):
    return render(request, 'profile.html')

def index(request):
    return render(request,'index.html')

@login_required
def member(request):
    members = Member.objects.all()  # Change variable name
    
    if request.method == "POST":
        try:
            user_id = request.POST.get('user')  # Assuming user ID is sent from form
            house_no = request.POST.get('house_no')

            user = User.objects.get(id=user_id)  # Get User instance

            member = Member.objects.create(user=user, house_no=house_no)
            member.save()
            messages.success(request, "Member added successfully!")

            return JsonResponse({'message': 'Member added successfully!'})
        except User.DoesNotExist:
            return JsonResponse({'message': 'User not found!'}, status=400)
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'An error occurred!'}, status=500)

    print(members)
    return render(request, 'society_m.html', {'members': members})  # Change key to 'members'

