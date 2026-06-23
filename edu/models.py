from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class student_signup_data(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    st_name = models.CharField()
    st_email = models.EmailField()
    st_username = models.CharField()
    st_password = models.CharField()
    st_confirm_pass = models.CharField()

class Subjects_details(models.Model):
    course_name = models.CharField()
    course_desc = models.CharField()
    no_of_students = models.IntegerField()
    months = models.IntegerField()
    Rating = models.IntegerField()
    price = models.CharField()

class enrollment_data(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments')
    first_name = models.CharField()
    last_name = models.CharField()
    email = models.EmailField()
    phone = models.CharField()
    dob = models.CharField()
    gender = models.CharField()
    current_class = models.IntegerField()
    school = models.CharField()
    course = models.CharField()
    parent_name = models.CharField()
    parent_phone = models.CharField()
    address = models.CharField()
    message = models.CharField()

# class Curriculum_data(models.Model):
#     subject_name = models.CharField()
#     subject_desc =  models.CharField()

# class curriculum_topic_name(models.Model):
#     curriculum_topic_names = models.CharField()

# class curriculum_topic_videos(models.Model):
#     v = models.CharField()
    
class Course(models.Model):
    subject_name = models.CharField(max_length=200)
    subject_desc = models.TextField()
    skills = models.CharField(max_length=300)
    skills_desc = models.TextField()

class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    heading = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0) 

class Topic(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='topics')
    name = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

class concepts_covered(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='concepts_covered')
    conc_cov = models.CharField(max_length=200)
    concept_desc = models.TextField()
    order = models.PositiveIntegerField(default=0)
    
