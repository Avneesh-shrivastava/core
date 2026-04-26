from django.db import models

# Create your models here.
class Students_data(models.Model):
    name = models.CharField()
    email_id = models.EmailField()
    phone_no = models.IntegerField()
    address = models.CharField()
    reason = models.CharField()

