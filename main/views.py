from django.shortcuts import render
from .module import Web_module
from django.core.paginator import Paginator
from .models import *
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

    htmls = ['result/prof.html', 'result/both.html', 'result/noMatch.html']
    html_selector = 0
    if lecture and professor: # 강의명으로 검색 시
        try:
            result = data_analyser.find_similar_lecture(lecture, professor)
        except:
            alert ="교수명과 강의명이 일치하지 않습니다."
            return render(request, "home.html", {'alert' : alert})
        else:
            html_selector = 1
            context.update({
                'lecture':lecture,
                'professor':professor,
                'result':result
            })


    elif professor != '' : #교수명만 검색시s
        html_selector = 0
        result = data_analyser.find_similar_prof(professor)
        context.update({
            'professor':professor,
            'result':result
            })
    elif professor == '' and lecture == '' :
        alert ="교수명과 강의명을 입력하세요."
        return render(request, "home.html", {'alert' : alert})

    return render(request, htmls[html_selector], context)



def show(request):
    lecture = request.GET.get('lecture') #강의명 검색 value
    professor = request.GET.get('professor') #교수명 검색 value
    result = data_analyser.find_similar_lecture(lecture, professor)

    reviews = result["review"].tolist()
    scores = 0
    for review in reviews:
        scores += review[1]
    average = round(scores/len(reviews), 2)


    lectures = Lecture.objects.filter(name=lecture, prof=professor)
    first_lecture = Lecture.objects.filter(name=lecture, prof=professor)[0]

    return render(request, 'result/show.html', {"result": result, "first_lecture": first_lecture, "lectures": lectures, "average": average})


