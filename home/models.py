from django.db import models

# Create your models here.
class student(models.Model):
    #id = models.AutoField()
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True, blank=True)
    email = models.EmailField()
    address = models.TextField(null=True, blank=True)
    
class cars(models.Model):
    car_name = models.CharField()
    car_type = models.CharField()
    

    def __str__(self) -> str:
        return self.car_name