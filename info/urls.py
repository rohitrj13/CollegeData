from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name="index"),
    path('logout/',views.logoutuser,name='logoutuser'),
    path('teacher/marks/<slug:teacher_id>',views.t_marks,name='t_marks'),
    path('teacher/exams/<int:ass_id>/',views.t_examselect,name='t_examselect'),
    path('teacher/entermarks/<slug:marks_id>',views.t_entermarks,name='t_entermarks'),
    path('teacher/editmarks/<slug:marks_id>',views.t_editmarks,name='t_editmarks'),
    path('teacher/marksconfirm/<int:marks_id>',views.confirm,name='confirm'),
    #path('teacher/contact/<int:marks_id>',views.contact,name='contact'),
    path('student/viewmarks',views.s_viewmarks,name='s_viewmarks'),

    #Attendance
    path('teacher/attendance',views.t_attendance,name='t_attendance'),
    path('teacher/selectdate/<slug:ass_id>',views.t_attendanceclasses,name='t_attendanceclasses'),
    path('teacher/enterattendance/<slug:attendanceclass_id>',views.t_enterattendance,name='t_enterattendance'),
    path('teacher/enterattendance/<slug:attendanceclass_id>/submit',views.submitattendance,name='submitattendance'),
    path('student/viewattendance',views.s_viewattendance,name='s_viewattendance'),

    #path('teacher/marksubmit/<int:ass_id>',views.confirm,name='confirm')

    #Assignment
    path('teacher/assignment',views.t_assignment,name='t_assignment'),
]
