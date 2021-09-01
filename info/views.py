from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Teacher, Student, Assign, Marks, MarksConfirm, GetMarks
# Create your views here.
from .models import AttendanceClass, Attendance,AttendanceTotal


@login_required
def index(request):
    if request.user.is_teacher:
        return render(request,'teacher.html')
    if request.user.is_student:
        return render(request,'student.html')
    return redirect('/admin')

def logoutuser(request):
    logout(request)
    return redirect('index')


def t_marks(request,teacher_id):
    teacher = Teacher.objects.get(id = teacher_id)
    return render(request,'t_marks.html',{'teacher':teacher})

def t_examselect(request,ass_id):
    ass = Assign.objects.get(id = ass_id)
    return render(request,'t_examselect.html',{'ass':ass})


def t_entermarks(request,marks_id):
    mark = Marks.objects.get(id = marks_id)
    assi = mark.ass
    cl = assi.class_id
    att = cl.student_set.all().order_by('-USN')
    att = att.reverse()
    print(att)
    return render(request,'t_entermarks.html',{'mark':mark,'assi':assi,'cl':cl,'att':att})

def t_editmarks(request, marks_id):
    mark = Marks.objects.get(id = marks_id)
    ex = mark.examname
    assi = mark.ass
    cl = assi.class_id
    cr = assi.course
    att = cl.student_set.all().order_by('-USN')
    print(att)
    att_list=[]
    for i in att:
        stud = Student.objects.get(USN = i.USN)
        MC = MarksConfirm.objects.filter(student=stud,course=cr,examname=ex)
        att_list.append(MC[0])
        print(MC[0].examname,MC[0].marksnumber)
    att_list.reverse()
    return render(request,'t_editmarks.html',{'att_list':att_list,'marks_id':marks_id})

def confirm(request,marks_id):
    mark = Marks.objects.get(id = marks_id)
    assi = mark.ass
    cl = assi.class_id
    cr = assi.course
    already_exists = MarksConfirm.objects.filter(course=cr,marks=mark,examname=mark.examname).count()
    print(already_exists)
    already_exists = MarksConfirm.objects.filter(course=cr,marks=mark,examname=mark.examname)
    for each in already_exists:
        each.delete()
    for i in cl.student_set.all():
        markss = request.POST.get(i.USN)
        if(markss!=None):
            a = MarksConfirm(course = cr,student=i,marksnumber=markss,examname=mark.examname,marks=mark)
        else:
            a = MarksConfirm(course = cr,student=i,marksnumber="absent",examname=mark.examname,marks=mark)
        a.save()
        print(a.marksnumber)
    mark.status = 1
    mark.save()
    return redirect('index')



    



examnames = {
    1:'Internal Exam 1',
    2:'Internal Exam 2',
    3:'Internal Exam 3',
    4:'External Exam',
}

def s_viewmarks(request):
    stud = Student.objects.get(USN = request.user.student.USN)
    cl = stud.class_id
    att = []
    for i in cl.assign_set.all():
        try:
            a = GetMarks.objects.get(student=stud,course = i.course)
        except GetMarks.DoesNotExist:
            a = GetMarks(student = stud,course = i.course)
            a.save()
        att.append(a)
    return render(request,'s_viewmarks.html',{'stud':stud,'cl':cl,'att':att})
    
    #Attendance From Here On
def t_attendance(request):
    teacher = Teacher.objects.get(id = request.user.teacher.id)
    ass = teacher.assign_set.all()
    return render(request,'t_attendance.html',{'ass':ass})

def t_attendanceclasses(request,ass_id):
    ass = Assign.objects.get(id = ass_id)
    att_list=[]
    att_list = ass.attendanceclass_set.all().order_by('-date')
    att_list = att_list.reverse()
    print(len(att_list))
    return render(request,'t_attendanceclasses.html',{'att_list':att_list})


def t_enterattendance(request,attendanceclass_id):
    print(attendanceclass_id)
    ac = AttendanceClass.objects.get(id = attendanceclass_id)
    ass = ac.assign
    cl = ass.class_id
    return render(request,'t_enterattendance.html',{'ac':ac,'ass':ass,'cl':cl})
    #ac="ROHIT"

def submitattendance(request,attendanceclass_id):
    ac = AttendanceClass.objects.get(id = attendanceclass_id)
    ass = ac.assign
    cl = ass.class_id
    cr = ass.course
    print("Well Its Okay")
    for i in cl.student_set.all():
        status = request.POST.get(i.USN)
        print(status)
        if status == 'present':
            status = True
        else:
            status = False
        a = Attendance(course = cr,student = i,status=status,attendanceclass=ac,date = ac.date)
        a.save()
    ac.status = 1
    ac.save()
    return redirect('index')

def s_viewattendance(request):
    cl = request.user.student.class_id
    print(cl)
    att_total = []
    for i in cl.assign_set.all():
        cr = i.course
        st = request.user.student
        try:
            a = AttendanceTotal.objects.get(student=st,course=cr)
        except AttendanceTotal.DoesNotExist:
            a = AttendanceTotal(student=st,course=cr)
            a.save()
        att_total.append(a)
    print(a.total_classes)
    return render(request,'s_viewattendance.html',{'cl':cl,'att_total':att_total})
    


#Assignment Questions
def t_assignment(request):
    teacher = Teacher.objects.get(id = request.user.teacher.id)
    return render(request,'t_assignment.html',{'teacher':teacher})