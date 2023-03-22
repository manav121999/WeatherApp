from django.urls import path
from weatherapp.views import celcius,fahrenheit

# Create your urls here

urlpatterns = [
    path('',celcius,name='celcius'),
    path('fahrenheit/',fahrenheit,name='fahrenheit'),
    
]
