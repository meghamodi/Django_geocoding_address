from django.db import models
from django.contrib.auth.models import User
from datetime import datetime



class Sheet(models.Model):
	user = models.ForeignKey(User,related_name='sheets',on_delete=models.CASCADE)
	file = models.FileField(max_length=65,upload_to='media/sheets/%Y/%m/%d')


# Create your models here.
