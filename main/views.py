from django.shortcuts import render, redirect
from .module import Web_module
from django.core.paginator import Paginator
from .models import *
from django.contrib.auth.decorators import login_required
from datetime import datetime


now = datetime.now()
semester = 0
if 6 > now.month >= 3:
    semester = 1  # 1학기
elif 12 > now.month >=9:
    semester = 2  # 2학기
current_semester = "%s%s" % (now.year, semester)

data_analyser = Web_module.similar()


def searchByLecture(lecture_name, professor_name):
    try:
        return data_analyser.find_similar_lecture(lecture_name, professor_name)
    except:
        return {"error": "리뷰가 부족하여 데이터를 확인할 수 없습니다."}

def searchByProfessor(professor_name):
    try:
        return data_analyser.find_similar_prof(professor_name)
    except:
        return {"error": "존재하지 않는 교수입니다."}

def home(request):
    lecture_list = list(set(list(Lecture.objects.values_list('name', flat=True))))
    professor_list = list(set(list(Lecture.objects.values_list('prof', flat=True))))

    return render(request, 'home.html',
        {
            "lecture_list": lecture_list,
            "professor_list": professor_list
        })

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
                'result':result,
            })


    elif professor != '' : #교수명만 검색시s
        html_selector = 0
        result = data_analyser.find_similar_prof(professor)
        filter = Lecture.objects.filter(prof=professor).order_by('name')
        lecture_of_prof = filter.values_list('name', flat=True).distinct()
        context.update({
            'professor':professor,
            'result':result,
            'lectures':lecture_of_prof,
            })
    elif professor == '' and lecture == '' :
        alert ="교수명과 강의명을 입력하세요."
        return render(request, "home.html", {'alert' : alert})

    return render(request, htmls[html_selector], context)



def show(request):
    lecture = request.GET.get('lecture') #강의명 검색 value
    professor = request.GET.get('professor') #교수명 검색 value

    context = dict()

    html_selector = 0
    htmls = ['result/show_lecture_detail.html', 'result/show_prof_detail.html']

    if lecture:
        html_selector = 0
        result = data_analyser.find_similar_lecture(lecture, professor)

        reviews = result["review"].tolist()
        scores = 0
        for review in reviews:
            scores += review[1]
        average = round(scores/len(reviews), 2)


        lectures = Lecture.objects.filter(name=lecture, prof=professor)
        first_lecture = Lecture.objects.filter(name=lecture, prof=professor)[0]

        likes_list = Like.objects.filter(user = request.user.id).values_list('lecture', flat=True).distinct()
        context.update({"result": result, "first_lecture": first_lecture, "lectures": lectures, "average": average,
         "likes_list": likes_list})
    else:
        html_selector = 1
        result = data_analyser.find_similar_prof(professor)

        filter = Lecture.objects.filter(prof=professor, semester__icontains=current_semester)
        lectures = filter.values_list('name').distinct()
        context.update({"result": result, "lectures": lectures})
    return render(request, htmls[html_selector], context)


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


def hashtag_search(keyword):
    prof_q = data_analyser.search_tags_prof(keyword)
    lecture_q = data_analyser.search_tags_lecture(keyword)
    prof_list = list(prof_q.keys())
    lecture_list = list(lecture_q.keys())
    return {'q':keyword, 'prof_q':prof_q, 'lecture_q' : lecture_q, 'prof_list': prof_list, 'lecture_list': lecture_list}


def search(request):
    q = request.GET.get('q')
    ctx = hashtag_search(q)
    return render(request, 'result/search.html', ctx)


def total_search(request):
    ctx = dict()
    keyword = request.GET.get('queryset')

    lectures = Lecture.objects.filter(name=keyword, semester__icontains=current_semester).order_by('prof').distinct()
    lectures = list(set(map(lambda x: x.name + " " + x.prof, lectures)))
    lectures = list(map(lambda x: [x.split()[0], x.split()[1]], lectures))

    professors = searchByProfessor(keyword)
    try:
        if professors['error']:
            professors = {}
    except:
        pass
    hashtags = hashtag_search(keyword)
    print(hashtags)
    ctx.update({
        'keyword': keyword,
        'lectures': lectures,
        'professors': professors,
        'hashtags': hashtags,
    })
    return render(request, 'result/total_search.html', ctx)

