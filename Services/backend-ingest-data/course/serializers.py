from rest_framework import serializers
from .models import Instructors,Terms, Courses, Sections, Schedules, Locations, InstructionMediums, Subjects

class InstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instructors
        fields = ['id', 'name']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courses
        fields = ['id', 'name', 'code','credits','subject_id','prereqs','coreqs','note']

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sections
        fields = ['crn', 'name', 'instructor_id', 'course_id', 'term_id', 'medium_id', 'is_active', 'is_lab', 'enrolled', 'capacity','note']

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedules
        fields = ['id', 'location_id', 'crn_id', 'is_weekly', 'weekday', 'time_start', 'time_end', 'date_start', 'date_end']

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locations
        fields = ['id', 'campus','building','room']

class InstructionMediumSerializer(serializers.ModelSerializer):
    class Meta:
        model = InstructionMediums
        fields = ['id', 'name']

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subjects
        fields = ['id', 'name']

class TermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Terms
        fields = ['id', 'name']