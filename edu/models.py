from django.db import models

# Create your models here.
class student_signup_data(models.Model):
    st_name = models.CharField()
    st_email = models.EmailField()
    st_username = models.CharField()
    st_password = models.CharField()
    st_confirm_pass = models.CharField()

