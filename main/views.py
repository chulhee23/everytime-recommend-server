from django.shortcuts import render
from .module import Web_module
# Create your views here.


data_analyser = Web_module.similar()


def searchByLecture(lecture_name, professor_name):
    return data_analyser.find_similar_lecture(lecture_name, professor_name)

def searchByProfessor(professor_name):
    return data_analyser.find_similar_prof(professor_name)


def home(request) :
    return render(request, 'home.html')

def temp(request):
    return render(request, 'temp.html')

def result(request):
    lecture = request.GET.get('lecture') #강의명 검색 value
    professor = request.GET.get('professor') #교수명 검색 value
    context = dict()

    htmls = ['result/prof.html', 'result/both.html']
    html_selector = 0
    if lecture and professor: # 강의명으로 검색 시
        html_selector = 1
        result = data_analyser.find_similar_lecture(lecture, professor)
        context.update({
            'lecture':lecture,
            'professor':professor,
            'result':result
            })
    elif professor != '' : #교수명만 검색시s
        html_selector = 1
        result = data_analyser.find_similar_prof(professor)
        context.update({
            'professor':professor,
            'result':result
            })
    return render(request, htmls[html_selector], context)
