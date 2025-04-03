from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm

from django.contrib.auth import get_user_model

User = get_user_model()  # This ensures you're using 'accounts.CustomUser'

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            response = redirect('resume-create')  # Redirect to Resume Creation Page
            response.set_cookie('gradpath_user', user.username)  
            return response
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            response = redirect('welcome')
            response.set_cookie('gradpath_user', user.username)
            return response
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def home_view(request):
    return render(request, 'home.html')


@login_required
def welcome_view(request):
    response = render(request, 'accounts/welcome.html')
    response.set_cookie('gradpath_user', request.user.username)  
    return response


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User

@login_required
def account_settings(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")

        # Validate email and username uniqueness
        if User.objects.filter(email=email).exclude(id=request.user.id).exists():
            messages.error(request, "This email is already registered with another account.")
        elif User.objects.filter(username=username).exclude(id=request.user.id).exists():
            messages.error(request, "This username is already taken. Please choose a different one.")
        else:
            request.user.username = username
            request.user.email = email
            request.user.save()
            messages.success(request, "Profile updated successfully!")

        # Handle password change
        password_form = SetPasswordForm(request.user, request.POST)
        if request.POST.get("new_password1") or request.POST.get("new_password2"):
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "Password updated successfully!")
                return redirect("account_settings")
            else:
                messages.error(request, "Password change failed. Please check your input.")
        else:
            # If no password change attempt, still pass an empty form for rendering
            password_form = SetPasswordForm(request.user)

    else:
        # GET request: show current settings and blank password form
        password_form = SetPasswordForm(request.user)

    return render(request, "account_settings.html", {"password_form": password_form})


from django.contrib.auth import get_user_model
from django.http import JsonResponse

User = get_user_model()  # Get the CustomUser model

def update_email(request):
    if request.method == "POST":
        email = request.POST.get("email")
        
        if User.objects.filter(email=email).exclude(id=request.user.id).exists():
            return JsonResponse({"error": "This email is already in use."}, status=400)

        # Proceed with updating email...
        request.user.email = email
        request.user.save()
        return JsonResponse({"message": "Email updated successfully!"})

    return JsonResponse({"error": "Invalid request"}, status=400)
