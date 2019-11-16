from django.db import models
from django.contrib.auth.models import User
# Create your models here.


# name, class_code, score, category, prof, time, recommend_year, weight, competitor, remarks, link, semester
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

class Like(models.Model):
    lecture = models.ForeignKey(Lecture, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

# class Review(models.Model):
#     pass