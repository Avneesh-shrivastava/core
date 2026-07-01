from django.db import models
from django.contrib.auth.models import User



# Create your models here.
class student_signup_data(models.Model): #this model stores the data of the user when user sign ups
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    st_name = models.CharField()
    st_email = models.EmailField()
    st_username = models.CharField()
    st_password = models.CharField()
    st_confirm_pass = models.CharField()

class Subjects_details(models.Model): #this model is used to show the data on every course cards
    course_name = models.CharField()
    course_desc = models.CharField()
    no_of_students = models.IntegerField()
    months = models.IntegerField()
    Rating = models.IntegerField()
    price = models.CharField()

class enrollment_data(models.Model): #when someone enrolls their data is stored here
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
    
class Course(models.Model): # This model is used to show the subject and skill details on the curriculum page
    subject_name = models.CharField(max_length=200)
    subject_desc = models.TextField()
    skills = models.CharField(max_length=300)
    skills_desc = models.TextField()

class Module(models.Model): #This model is used to show the topic title on the course curriculum block  
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    heading = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0) 

class Topic(models.Model): # This model is used to show the video topics in different Modules
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='topics')
    name = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

class concepts_covered(models.Model): # This model is used to show the details of "skills and concepts covered in this course"
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='concepts_covered')
    conc_cov = models.CharField(max_length=200)
    concept_desc = models.TextField()
    order = models.PositiveIntegerField(default=0)

class user_n_course(models.Model): # This model stores the user_id and course_id of the user who has enrolled 
    user =  models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_n_course')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='user_n_course')

class topic_links(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='topics_links')
    url = models.CharField()
