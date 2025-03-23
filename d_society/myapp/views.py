from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import User, Chairman, Member, Watchman
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import ValidationError
from django.db import transaction
from django.contrib.auth.hashers import make_password  # For password hashing
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import logging
from django.shortcuts import get_object_or_404, redirect

logger = logging.getLogger(__name__)

# Home view
def home(request):
    return render(request, 'dashboard.html')

# Register view
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import User
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def register(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        role = request.POST.get('role')
        
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return render(request, 'register.html')

        # Check if phone number already exists
        if User.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number already exists!")
            return render(request, 'register.html')


        try:
            # Create the user with password hashing
            user = User.objects.create(
                username=username,
                email=email,
                phone=phone,
                role=role,
                password=password,  # Hash the password
                
            )
            user.save()

            messages.success(request, "Registration successful!")
            return redirect('login')  # Redirect to login page after successful registration

        except Exception as e:
            messages.error(request, "An error occurred during registration.")
            print(f"Error: {e}")  # Log the error for debugging purposes
            return render(request, 'register.html')

    else:
        return render(request, 'register.html')

# Login view
@csrf_protect
def User_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Retrieve the user by email
            user = User.objects.get(email=email)

            # Check if the provided password matches the stored password
            if user.password == password:
                request.session['email'] = user.email  # Store email in session
                print("Login view accessed")
                # Redirect to the next URL if it exists, otherwise redirect to a default page
                next_url = request.GET.get('next', 'member')  # Default to 'society' if no next parameter
                return redirect(next_url)

            else:
                logger.warning('Invalid password for email: %s', email)
                return render(request, 'login.html', {'error': 'Invalid password!'})

        except User.DoesNotExist:
            logger.warning('User  does not exist for email: %s', email)
            return render(request, 'login.html', {'error': 'User  does not exist'})
        except Exception as e:
            logger.error(f"An error occurred: {str(e)}")
            return render(request, 'login.html', {'error': 'An error occurred'})

    return render(request, 'login.html')

# Logout view
@login_required
def custom_logout(request):
    user = request.user
    user.is_active = False  # Deactivate the user
    user.save()
    logout(request)
    return redirect('login')  # Redirect to login page or homepage

# Profile view
def profile(request):
    return render(request, 'profile.html')

# Index view
def index(request):
    return render(request, 'index.html')

# Member view (Listing and adding members)

def member(request):
    members = Member.objects.all()  # Fetch all members

    if request.method == "POST":
        username = request.POST.get('username')  # Get username from form
        house_no = request.POST.get('house_no')

        if not username or not house_no:
            return JsonResponse({'message': 'Username and house number are required!'}, status=400)

        try:
            # Try to get the user by username
            user, created = User.objects.get_or_create(username=username)

            # If the user was just created, you might want to set additional fields
            if created:
                # Optionally set other fields for the new user
                user.email = f"{username}@example.com"  # Example email, adjust as needed
                user.set_password('defaultpassword')  # Set a default password or handle it differently
                user.save()

            # Check if the user already has a member profile
            if Member.objects.filter(user=user).exists():
                messages.error(request, "This user is already a member.")
                return redirect("member")

            # Create the new member
            member = Member.objects.create(user=user, house_no=house_no)
            member.save()
            messages.success(request, "Member added successfully!")

            return JsonResponse({'message': 'Member added successfully!'})
        except Exception as e:
            print("Error:", e)  # It's good to log the error instead of just printing
            return JsonResponse({'message': 'An error occurred!'}, status=500)

    return render(request, 'society_m.html', {'members': members})  # Pass members to template

def add_watchman(request):
    watchmen = Watchman.objects.all()  # Fetch all watchmen
    
    if request.method == "POST":
        username = request.POST.get('username')  # Get username from form
        shift = request.POST.get('shift')  # Get shift from form

        if not username or not shift:
            return JsonResponse({'message': 'Username and shift are required!'}, status=400)

        try:
            # Try to get the user by username
            user, created = User.objects.get_or_create(username=username)

            # If the user was just created, you might want to set additional fields
            if created:
                user.email = f"{username}@example.com"  # Example email, adjust as needed
                user.set_password('defaultpassword')  # Set a default password or handle it differently
                user.save()

            # Check if the user already has a watchman profile
            if Watchman.objects.filter(user=user).exists():
                messages.error(request, "This user is already a watchman.")
                return redirect("add_watchman")  # Redirect to the same page

            # Create the new watchman
            watchman = Watchman.objects.create(user=user, shift=shift)
            watchman.save()
            messages.success(request, "Watchman added successfully!")

            return JsonResponse({'message': 'Watchman added successfully!'})
        except Exception as e:
            print("Error:", e)  # It's good to log the error instead of just printing
            return JsonResponse({'message': 'An error occurred!'}, status=500)

    return render(request, 'watchmen.html',{'watchmen': watchmen})  # Render the form template

def edit_watchman(request, watchman_id):
    watchman = get_object_or_404(Watchman, id=watchman_id)  # Fetch the watchman instance

    if request.method == "POST":
        shift = request.POST.get('shift')  # Get the updated shift from the form

        if not shift:
            messages.error(request, "Shift is required!")
            return redirect("edit_watchman", watchman_id=watchman.id)

        watchman.shift = shift  # Update the shift
        watchman.save()  # Save the changes
        messages.success(request, "Watchman updated successfully!")
        return redirect("add_watchman")  # Redirect to the watchman list

    return render(request, 'edit_watchman.html', {'watchman': watchman})  # Render the edit form

def delete_watchman(request, watchman_id):
    watchman = get_object_or_404(Watchman, id=watchman_id)  # Fetch the watchman instance
    watchman.delete()  # Delete the watchman
    messages.success(request, "Watchman deleted successfully!")
    return redirect("add_watchman")  # Redirect to the watchman list


# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Notice, Event
from django.contrib.auth.decorators import login_required


def notice_list(request):
    notices = Notice.objects.all()
    return render(request, 'notice_list.html', {'notices': notices})


def add_notice(request):
    if request.method == "POST":
        title = request.POST.get('title')  # Get notice title from form
        content = request.POST.get('content')  # Get notice content from form

        if not title or not content:
            messages.error(request, "All fields are required!")
            return redirect('add_notice')  # Redirect back to the form

        try:
            # Ensure request.user is a User instance
             # This should be a User instance

           
            notice = Notice.objects.create(
                title=title,
                content=content,
                
            )
            messages.success(request, "Notice added successfully!")
            return redirect('notice_list')  # Redirect to the notice list or another page
        except Exception as e:
            print("Error:", e)  # It's good to log the error instead of just printing
            messages.error(request, "An error occurred while adding the notice.")
            return redirect('notice_list')  # Redirect back to the form

    return render(request, 'notice_list.html')  # Render the form template



def delete_notice(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id)
    notice.delete()
    messages.success(request, "Notice deleted successfully!")
    return redirect('notice_list')

def add_event(request):
    if request.method == "POST":
        title = request.POST.get('title')  # Get event title from form
        description = request.POST.get('description')  # Get event description from form
        event_date = request.POST.get('event_date')  # Get event date from form
        location = request.POST.get('location')  # Get event location from form

        if not title or not description or not event_date or not location:
            messages.error(request, "All fields are required!")
            return redirect('add_event')  # Redirect back to the form

        try:
            # Ensure request.user is a User instance
            user = request.user if request.user.is_authenticated else None

            # Create the new event
            event = Event.objects.create(
                title=title,
                description=description,
                event_date=event_date,
                location=location,
            )
            messages.success(request, "Event added successfully!")
            return redirect('event_list')  # Redirect to the event list or another page
        except Exception as e:
            print("Error:", e)  # It's good to log the error instead of just printing
            messages.error(request, "An error occurred while adding the event.")
            return redirect('event_list')  # Redirect back to the form

    return render(request, 'event_list.html')  # Render the form template



def event_list(request):
    events = Event.objects.all()
    return render(request, 'event_list.html', {'events': events})


def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)   
    event.delete()
    messages.success(request, "Event deleted successfully!")
    return redirect('event_list')