from django.contrib import admin
from .models import Schedules, Sections, Subjects, InstructionMediums, Instructors, Courses, Locations, Terms

# Register your models here.
admin.site.register(Schedules)
admin.site.register(Sections)
admin.site.register(Subjects)
admin.site.register(InstructionMediums)
admin.site.register(Instructors)
admin.site.register(Courses)
admin.site.register(Locations)
admin.site.register(Terms)