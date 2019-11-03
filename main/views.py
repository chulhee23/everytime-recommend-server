from django.shortcuts import render
# from .analyze import Web_module
# Create your views here.
def home(request) :
    # Web_module.similar().question()

    return render(request, 'home.html')

def temp(request):
    return render(request, 'temp.html')

def result(request):
    lecture = request.GET.get('lecture') #강의명 검색 value
    professor = request.GET.get('professor') #교수명 검색 value

    if lecture != '' and professor != '' : #둘 다 검색시
        return render(request, 'result/both.html', {'lecture': lecture, 'professor':professor})
    elif lecture != '' and professor == '' : #강의명만 검색시
        return render(request, 'result/lecture.html', {'lecture': lecture})
    elif lecture == '' and professor != '' : #교수명만 검색시
        return render(request, 'result/prof.html', {'professor':professor})