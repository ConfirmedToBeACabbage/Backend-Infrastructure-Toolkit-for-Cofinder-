from django.db import models

# Create your models here.
class Instructors(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=64)

    def __str__(self):
        return "%s" % (self.name)

class Subjects(models.Model):
    id = models.CharField(max_length=8, primary_key=True)
    name = models.CharField(max_length=64)

    def __str__(self):
        return "%s" % (self.name)

class Terms(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=32)

    def __str__(self):
        return "%s" % (self.name)

class Courses(models.Model):
    id = models.UUIDField(primary_key=True)
    code = models.CharField(max_length=8)
    name = models.CharField(max_length=128)
    credits = models.FloatField()
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    prereqs = models.TextField()
    coreqs = models.TextField()
    note = models.TextField()

    def __str__(self):
        return "%s %s - %s (%s)" % (self.subject, self.code, self.name, self.credits)

class InstructionMediums(models.Model):
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=128)

    def __str__(self):
        return "%s" % (self.name)

class Sections(models.Model):
    crn = models.IntegerField(primary_key=True)
    instructor = models.ForeignKey(Instructors,on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=16)
    course = models.ForeignKey(Courses,on_delete=models.CASCADE)
    term = models.ForeignKey(Terms, on_delete=models.CASCADE)
    medium = models.ForeignKey(InstructionMediums, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    is_lab = models.BooleanField(default=False)
    enrolled = models.IntegerField()
    capacity = models.IntegerField()
    note = models.TextField()

    def __str__(self):
        return "%s  %s - %s - %s %s - %s (Active: %s, Is Lab: %s)" % (self.crn, self.name, self.instructor.name, self.course.subject, self.course.code, self.term.name, self.is_active, self.is_lab)

class Locations(models.Model):
    id = models.UUIDField(primary_key=True)
    campus = models.CharField(max_length=64)
    building = models.CharField(max_length=64)
    room = models.CharField(max_length=8)

    def __str__(self):
        return "%s  %s  %s" % (self.campus, self.building, self.room)

class Schedules(models.Model):
    id = models.UUIDField(primary_key=True)
    location = models.ForeignKey(Locations, on_delete=models.SET_NULL, null=True)
    crn = models.ForeignKey(Sections, on_delete=models.CASCADE)
    is_weekly = models.BooleanField(default=True)
    weekday = models.CharField(max_length=1)
    time_start = models.IntegerField()
    time_end = models.IntegerField()
    date_start = models.IntegerField()
    date_end = models.IntegerField()

    def __str__(self):
        return "%s  (Weekly: %s)    - %s, from %s to %s" % (self.crn, self.is_weekly, self.weekday, self.date_start, self.date_end)
