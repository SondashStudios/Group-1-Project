from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm


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
from django.contrib.auth.models import User

@login_required
def account_settings(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")

        if User.objects.filter(email=email).exclude(id=request.user.id).exists():
            messages.error(request, "This email is already registered with another account.")
        else:
            request.user.username = username
            request.user.email = email
            request.user.save()
            messages.success(request, "Profile updated successfully!")

        return redirect("account_settings")

    return render(request, "account_settings.html")
