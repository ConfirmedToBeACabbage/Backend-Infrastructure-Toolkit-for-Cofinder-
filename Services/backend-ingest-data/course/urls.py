from django.urls import path
from .views import pushData, getInstructors, getCourses, \
        getInstructionMediums, getLocations, getSchedules,\
        getSections, getSubjects, getTermSections, getTerms

urlpatterns = [
    path('api/push/', pushData),
    path('api/instructors/', getInstructors),
    path('api/courses/', getCourses),
    path('api/subjects/', getSubjects),
    path('api/instructionmediums/', getInstructionMediums),
    path('api/locations/', getLocations),
    path('api/sections/', getSections),
    path('api/schedules/', getSchedules),
    path('api/terms/', getTerms),
    path('api/<termid>/sections/', getTermSections)
]