from django.shortcuts import render

# Create your views here.
def home(request) :
    return render(request, 'home.html')

def temp(request):
    return render(request, 'temp.html')

def result(request):
    lecture = request.GET.get('lecture') #강의명 검색 value
    professor = request.GET.get('professor') #교수명 검색 value

    if lecture != '' and professor != '' : #둘 다 검색시
        return render(request, 'resultBoth.html', {'lecture': lecture, 'professor':professor})
    elif lecture != '' and professor == '' : #강의명만 검색시
        return render(request, 'resultLecture.html', {'lecture': lecture})
    elif lecture == '' and professor != '' : #교수명만 검색시
        return render(request, 'resultProf.html', {'professor':professor})