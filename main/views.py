from django.shortcuts import render

# Create your views here.
def home(request) :
    return render(request, 'home.html')

def temp(request):
    return render(request, 'temp.html')

def result(request, type):
    
    return render(request, 'result.html')