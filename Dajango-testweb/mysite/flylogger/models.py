from django.db import models
from django_tables2 import SingleTableView

class Person(models.Model):
   name = models.CharField(max_length=100, verbose_name="Full name")



# Create your models here.
