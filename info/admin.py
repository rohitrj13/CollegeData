from django.contrib import admin
from .models import Dept, Class, Student, Teacher, User, Course, Assign
from django.contrib.auth.admin import UserAdmin
from .models import AssignTime
# Register your models here.

class AssignTimeInline(admin.TabularInline):
    model = AssignTime
    extra = 0

class AssignAdmin(admin.ModelAdmin):
    inlines = [AssignTimeInline]
    list_display = ('class_id','course','teacher')


admin.site.register(User,UserAdmin)
admin.site.register(Dept)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Course)
admin.site.register(Class)
admin.site.register(Assign,AssignAdmin)
