from django.shortcuts import render
from django.db import connections
# RestFramework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .parse_save import parseData
from .serializers import *
from .models import *

# Create your views here.
@api_view(['POST'])
def pushData(request):
    result = parseData(request.FILES['file'],request.data['term'])
    return Response(data=result, status=status.HTTP_200_OK)

@api_view(['GET'])
def getSubjects(request):
    subjectSerializer = SubjectSerializer(Subjects.objects.all().values(), many=True)
    return Response(data=subjectSerializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def getInstructors(request):
    instructorSerializer = InstructorSerializer(Instructors.objects.all().values(), many=True)
    return Response(data=instructorSerializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def getCourses(request):
    courseSerializer = CourseSerializer(Courses.objects.all().values(), many=True)
    return Response(data=courseSerializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def getSections(request):
    sectionSerializer = SectionSerializer(Sections.objects.all().values(), many=True)
    return Response(data=sectionSerializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def getSchedules(request):
    scheduleSerializer = ScheduleSerializer(Schedules.objects.all().values(), many=True)
    return Response(data=scheduleSerializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def getLocations(request):
    locationSerializer = LocationSerializer(Locations.objects.all().values(), many=True)
    return Response(data=locationSerializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def getInstructionMediums(request):
    instructionMediumSerializer = InstructionMediumSerializer(InstructionMediums.objects.all().values(), many=True)
    return Response(data=instructionMediumSerializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def getTerms(request):
    termSerializer = TermSerializer(Terms.objects.all().values(), many=True)
    return Response(data=termSerializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def getTermSections(request, termid):
    sections = Sections.objects.select_related('course','instructor','medium','term').filter(term=termid)
    # Get data from foreign keys
    result = list()
    for section in sections:
        row = dict(course=CourseSerializer(section.course).data,
                   instructor=InstructorSerializer(section.instructor).data,
                   medium=InstructionMediumSerializer(section.medium).data
                   )
        schedules = Schedules.objects.select_related('location').filter(crn=section.crn)
        schList= list()
        for schedule in schedules:
            schRow = dict(location=LocationSerializer(schedule.location).data)
            schList.append({**schRow,**ScheduleSerializer(schedule).data})
        result.append({**row, **SectionSerializer(section).data,'schedule':schList})
    return Response(data={'data':result}, status=status.HTTP_200_OK)