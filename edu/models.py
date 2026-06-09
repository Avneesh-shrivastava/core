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
