from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=100, verbose_name="Lasse gunnar, Robert,")

# Create your models here.
