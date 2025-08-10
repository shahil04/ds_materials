from django.urls import path
from .views import courses

urlpatterns = [
    path('', courses, name='courses'),
]
