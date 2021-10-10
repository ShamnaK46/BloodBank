from django.db import models



class Data(models.Model):
    name = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)
    address = models.TextField(max_length=50)
    bloodgroup = models.CharField(max_length=10)
