# from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # ← これを追加
    student_id = models.AutoField(max_length=20, primary_key=True)
    student_name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.student_name


class Subject(models.Model):
    SUBJECT_CLASS_CHOICES = [
        ('必修', '必修'),
        ('教養', '教養'),
        ('専門', '専門'),
    ]

    DAY_CHOICES = [
    ('月', '月曜日'),
    ('火', '火曜日'),
    ('水', '水曜日'),
    ('木', '木曜日'),
    ('金', '金曜日'),
    ]

    day_of_week = models.CharField(max_length=2, choices=DAY_CHOICES, default='月')

    subject_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject_name = models.CharField(max_length=50)
    subject_class = models.CharField(max_length=10, choices=SUBJECT_CLASS_CHOICES)
    subject_score = models.IntegerField(default=1)
    subject_count = models.IntegerField(default=0)
    lesson_days = models.IntegerField(default=15)
    attend_days = models.IntegerField(default=0)
    lesson_count = models.IntegerField(default=0)
    date = models.CharField(max_length=10, default="月曜日")  # 曜日
    table = models.CharField(max_length=10, default="1限目")  # 時間割

    def __str__(self):
        return self.subject_name


class GPA(models.Model):
    gpa_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    gpa = models.FloatField(default=0.0)

    def __str__(self):
        return f'{self.student.student_name} - GPA: {self.gpa}'
