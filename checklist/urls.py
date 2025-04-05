from django.urls import path
from . import views  # Imports views file

urlpatterns = [
    path('', views.checklist_view, name='checklist'),
]
