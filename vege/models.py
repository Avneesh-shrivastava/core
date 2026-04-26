from django.db import models

# Create your models here.
class Receipe(models.Model):
    receipe_name = models.CharField()
    receipe_desc = models.CharField()
    receipe_image= models.ImageField(upload_to = "receipe")
    