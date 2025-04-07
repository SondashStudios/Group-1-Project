from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static


def home_redirect(request):
    return redirect('accounts/signup/')  # Redirects `/` to the signup page

def login_redirect(request):
    return redirect('api/v1/create/')  # Redirect to resume creation


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('api/v1/', include('resumes.urls')),
    path('', home_redirect, name='home'),
    path('accounts/profile/', login_redirect),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    