from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Institution(models.Model):
    # Wybór typów instytucji
    INSTITUTION_TYPES = (
        ('fundacja', 'Fundacja'),
        ('organizacja', 'Organizacja pozarządowa'),
        ('zbiórka_lokalna', 'Zbiórka lokalna'),
    )

    name = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=20, choices=INSTITUTION_TYPES, default='fundacja')
    categories = models.ManyToManyField('Category', related_name='institutions')

    def __str__(self):
        return self.name


class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField('Category')
    institution = models.ForeignKey('Institution', on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=10)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)