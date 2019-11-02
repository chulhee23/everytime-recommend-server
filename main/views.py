from django.shortcuts import render
from .analyze import Web_module
# Create your views here.
def home(request) :
    Web_module.similar().question()
    return render(request, 'home.html')

def temp(request):
    return render(request, 'temp.html')

def result(request, type):
    
    return render(request, 'result.html')