from django.shortcuts import render, redirect
from .module import Web_module
from django.core.paginator import Paginator
from .models import *
from django.contrib.auth.decorators import login_required
# Create your views here.


data_analyser = Web_module.similar()


def searchByLecture(lecture_name, professor_name):
    return data_analyser.find_similar_lecture(lecture_name, professor_name)

def searchByProfessor(professor_name):
    return data_analyser.find_similar_prof(professor_name)


def home(request):


    return render(request, 'home.html')

def temp(request):
    return render(request, 'temp.html')

@login_required
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

    likes_list = Like.objects.filter(user = request.user.id).values_list('lecture', flat=True).distinct()

    return render(request, 'result/show.html', {"result": result, "first_lecture": first_lecture, "lectures": lectures, "average": average, "likes_list": likes_list})



def like(request, lecture_id):
    current_user_id  = request.user.id
    lecture = Lecture.objects.get(id=lecture_id)

    likes = Like.objects.filter(lecture = lecture_id, user = request.user.id)
    if len(likes) == 0:
        like = Like()
        like.user = request.user
        like.lecture = lecture
        like.save()
    else:
        likes.delete()
    return redirect('mypage')


def mypage(request):
    likes = Like.objects.filter(user = request.user.id)
    return render(request, "users/mypage.html", {"likes": likes})
    #
    # postLike = PostLike.objects.filter(likedpost=post_id)
    # #라이커에 내가 있으면 그냥 리다이렉트
    # for liker in postLike:
    #     if liker.postliker == request.user:
    #         return redirect('home')
    #
    # newLike = PostLike()
    # newLike.postliker = request.user
    # likedPost = get_object_or_404(Post, pk=post_id)
    # newLike.likedpost = likedPost
    # likedPost.like += 1
    # likedPost.save()
    # newLike.save()
    # return redirect('home')
    #
    #
