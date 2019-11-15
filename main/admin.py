from django.contrib import admin
from .models import Lecture


# Register your models here.
class LectureAdmin(admin.ModelAdmin):
    list_display = ['name', 'prof', 'class_code']
admin.site.register(Lecture, LectureAdmin)