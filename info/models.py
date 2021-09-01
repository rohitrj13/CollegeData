from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import timedelta, date
from django.db.models.signals import post_save,post_delete
# Create your models here.
#



sex_choice = (
    ('Male', 'Male'),
    ('Female', 'Female')
)


class User(AbstractUser):
    @property
    def is_student(self):
        if hasattr(self,'student'):
            return True
        return False

    @property
    def is_teacher(self):
        if hasattr(self,'teacher'):
            return True
        return False



class Dept(models.Model):
    id = models.CharField(primary_key=True,max_length=20)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.id
    

class Class(models.Model):
    id = models.CharField(primary_key=True,max_length=20)
    dept = models.ForeignKey(Dept,on_delete=models.CASCADE)
    section = models.CharField(max_length=20)
    sem = models.IntegerField()

    class Meta:
        verbose_name_plural = 'Classes'

    def __str__(self):
        d = Dept.objects.get(id=self.dept)
        return '%s : %d %s' % (d.name, self.sem, self.section)


class Course(models.Model):
    dept = models.ForeignKey(Dept,on_delete=models.CASCADE)
    id = models.CharField(primary_key=True,max_length=20)
    name = models.CharField(max_length=50)
    shortname = models.CharField(max_length = 50)

    def __str__(self):
        return self.shortname
#    
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null = True)
    dept = models.ForeignKey(Dept,on_delete = models.CASCADE,default = 'CSE')
    class_id = models.ForeignKey(Class,on_delete = models.CASCADE)
    USN = models.CharField(primary_key=True,max_length = 50)
    name = models.CharField(max_length=50)
    sex = models.CharField(max_length=10,choices = sex_choice,default='Male')
    DOB = models.DateField(default='1999-01-01')
    
    def __str__(self):
        return self.name


class Teacher(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE, null=True)
    name = models.CharField(max_length=50)
    sex = models.CharField(max_length=10,choices = sex_choice,default='Female')
    id = models.CharField(primary_key=True,max_length=50)
    DOB = models.DateField(default='1990-01-01')
    dept = models.ForeignKey(Dept,on_delete = models.CASCADE,default='CSE')

    def __str__(self):
        return self.name

class Assign(models.Model):
    class_id = models.ForeignKey(Class,on_delete = models.CASCADE)
    course = models.ForeignKey(Course,on_delete = models.CASCADE)
    teacher = models.ForeignKey(Teacher,on_delete = models.CASCADE)

    class Meta:
        unique_together = (('course','class_id','teacher'),)

    def __str__(self):
        cl = Class.objects.get(id = self.class_id_id)
        cr = Course.objects.get(id = self.course_id)
        te = Teacher.objects.get(id=self.teacher_id)
        return '%s : %s : %s' % (te.name,cr.shortname,cl)
    

examnames = {
    1:'Internal Exam 1',
    2:'Internal Exam 2',
    3:'Internal Exam 3',
    4:'External Exam',
}

class Marks(models.Model):
    ass = models.ForeignKey(Assign,on_delete = models.CASCADE)
    examname = models.CharField(max_length=20)
    status = models.CharField(max_length=10,default='0')
    

def create_marks(sender,instance, **kwargs):
    if kwargs['created']:
        for i in range(1,5):
            a = Marks(examname = examnames[i],status='0',ass=instance)
            a.save()

class MarksConfirm(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    marks = models.ForeignKey(Marks,on_delete=models.CASCADE)
    examname = models.CharField(max_length = 20)
    #att = models.BooleanField(default='True')
    #status = models.CharField(max_length=20,default='not marked')
    marksnumber = models.CharField(max_length=10,default='0')

class GetMarks(models.Model):
    student = models.ForeignKey(Student,on_delete = models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)

    class Meta:
        unique_together = (('student','course'),)

    @property
    def IE1(self):
        stud = Student.objects.get(USN = self.student.USN)
        cr = Course.objects.get(shortname = self.course)
        markss = MarksConfirm.objects.filter(student=stud,course=cr,examname = 'Internal Exam 1')
        if(len(markss)!=0):
            return markss[0].marksnumber
        return "Not Marked"
    
    @property
    def IE2(self):
        stud = Student.objects.get(USN = self.student.USN)
        cr = Course.objects.get(shortname = self.course)
        markss = MarksConfirm.objects.filter(student=stud,course=cr,examname = 'Internal Exam 2')
        if(len(markss)!=0):
            return markss[0].marksnumber
        return "Not Marked"

    @property
    def IE3(self):
        stud = Student.objects.get(USN = self.student.USN)
        cr = Course.objects.get(shortname = self.course)
        markss = MarksConfirm.objects.filter(student=stud,course=cr,examname = 'Internal Exam 3')
        if(len(markss)!=0):
            return markss[0].marksnumber
        return "Not Marked"

    @property
    def EE(self):
        stud = Student.objects.get(USN = self.student.USN)
        cr = Course.objects.get(shortname = self.course)
        markss = MarksConfirm.objects.filter(student=stud,course=cr,examname = 'External Exam')
        if(len(markss)!=0):
            return markss[0].marksnumber
        return "Not Marked"

post_save.connect(create_marks,sender = Assign)
    #Attendance from here on

time_slots = (
    ('9:30-10:30','9:30-10:30'),
    ('11:00-12:00','11:00-12:00'),
    ('1:00-2:00','1:00-2:00'),
    ('2:30-3:30','2:30-3:30'),
)

days_of_week = (
    ('Monday','Monday'),
    ('Tuesday','Tuesday'),
    ('Wednesday','Wednesday'),
    ('Thursday','Thursday'),
    ('Friday','Friday'),
    ('Saturday','Saturday')
)

class AssignTime(models.Model):
    assign = models.ForeignKey(Assign,on_delete = models.CASCADE)
    period = models.CharField(max_length=20,choices = time_slots)
    day = models.CharField(max_length = 10,choices = days_of_week)

days = {
    'Monday':1,
    'Tuesday':2,
    'Wednesday':3,
    'Thursday':4,
    'Friday':5,
    'Saturday':6
}

def daterange(start_date,end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

def create_attendance(sender,instance,**kwargs):
    if kwargs['created']:
        start_date = date(2020, 9, 1)
        end_date = date(2021, 2, 1)
        for single_date in daterange(start_date,end_date):
            if single_date.isoweekday() == days[instance.day]:
                a = AttendanceClass(date = single_date.strftime("%Y-%m-%d"),assign = instance.assign)
                a.save()
                
class AttendanceClass(models.Model):
    assign = models.ForeignKey(Assign,on_delete = models.CASCADE)
    date = models.DateField()
    status = models.IntegerField(default=0)

post_save.connect(create_attendance,sender = AssignTime)

class Attendance(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete = models.CASCADE)
    status = models.BooleanField(default = True)
    attendanceclass = models.ForeignKey(AttendanceClass,on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return self.student+" "+self.course+" "+self.date+" "+self.status

class AttendanceTotal(models.Model):
    student = models.ForeignKey(Student,on_delete = models.CASCADE)
    course = models.ForeignKey(Course,on_delete = models.CASCADE)

    @property
    def total_classes(self):
        stud = Student.objects.get(USN = self.student.USN)
        cr = Course.objects.get(id = self.course.id)
        total_class = Attendance.objects.filter(student=stud,course=cr).count()
        return total_class
    
    @property
    def classes_attended(self):
        stud = Student.objects.get(USN = self.student.USN)
        cr = Course.objects.get(id = self.course.id)
        class_attended = Attendance.objects.filter(student=stud,course=cr,status=True).count()
        return class_attended

    @property
    def attendance_percentage(self):
        if (self.total_classes == 0):
            return 0
        return (self.classes_attended/self.total_classes)*100




