from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    #Come back to add images
    seller = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name