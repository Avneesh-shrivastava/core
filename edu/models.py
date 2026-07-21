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
    price = models.DecimalField(max_digits=8, decimal_places=2, default=5000) 
    original_price = models.DecimalField(max_digits=8, decimal_places=2, default=3999)

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
    is_free = models.BooleanField(default=False)


class Order(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='orders')
    
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2)
    original_price = models.DecimalField(max_digits=8, decimal_places=2)
    discount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    coupon_code = models.CharField(max_length=50, blank=True, null=True)
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    ordered_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.course.subject_name} - {self.status}"

class VideoProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    topic_link = models.ForeignKey(topic_links, on_delete=models.CASCADE, related_name='progress')
    watched = models.BooleanField(default=False)
    watched_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'topic_link')

    def __str__(self):
        return f"{self.user.username} - {self.topic_link.topic.name} - {self.watched}"