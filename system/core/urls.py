from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from . import views

app_name = 'core'  # 名前空間を設定

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('student_home/', views.student_home, name='student_home'),
    path('manage_grades/', views.manage_grades, name='manage_grades'),
    path('subject_register/', views.subject_register, name='subject_register'),
    path('grade_view/', views.grade_view, name='grade_view'),
    path('attendance_plan/', views.attendance_plan, name='attendance_plan'),
    path('register/', views.register_student, name='register_student'),
    path('register/class_count/', views.class_count_register, name='class_count_register'), #授業回数登録
    path('register/attendance/', views.attendance_register, name='attendance_register'),    #出席回数登録
    path('register/grade/', views.grade_register, name='grade_register'),                   #成績登録
    # path("subject/edit/<int:subject_id>/", views.subject_edit, name="subject_edit"),
    # path("subject/delete/<int:subject_id>/", views.subject_delete, name="subject_delete"),
]