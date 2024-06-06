from django.db import models

from users.models import User


class Stadion(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    price = models.IntegerField()
    location_lat = models.DecimalField(max_digits=9, decimal_places=6)
    location_lng = models.DecimalField(max_digits=9, decimal_places=6)
    description = models.TextField(default='')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stadions')

    def __str__(self):
        return self.name


class Photo(models.Model):
    stadion = models.ForeignKey(Stadion, related_name='photos', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='stadions')

    def __str__(self):
        return self.stadion.name
