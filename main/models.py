from django.db import models

# Create your models here.

# name, class_code, score, category, prof, time, recommend_year, weight, competitor, remarks, link, semester
# a = {"name": "군사학", "class_code": "032343-01", "score": 0.0, "category": "일반선택", "prof": "양동휘", 
# "time": "목 0(08:00-08:50) [학군단A동1층11호실],목 1(09:00-09:50) [학군단A동1층11호실],금 5(13:00-13:50) [7호관1층15호실],금 6(14:00-14:50) [7호관1층15호실],금 7(15:00-15:50) [7호관1층15호실],금 8(16:00-16:50) [7호관1층15호실]", 
# "recommend_year": "", 
# "weight": 3, 
# "competitor": 0, 
# "remarks": "ROTC 학생", 
# "link": "https://everytime.kr/lecture/view/546325", 
# "semester": "['20142', '20141']"}]

class Lecture(models.Model):
    name = models.CharField(max_length=100)
    class_code = models.CharField(max_length=100)
    score = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    prof = models.CharField(max_length=50)
    time = models.TextField()
    recommend_year = models.CharField(max_length=255)
    weight = models.CharField(max_length=100)
    remarks = models.TextField()
    link = models.URLField(max_length=255)
    semester = models.CharField(max_length=255)
    competitor = models.CharField(max_length=255, default="0")
