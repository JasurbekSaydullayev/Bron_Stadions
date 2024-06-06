from django.db import models

from stadions.models import Stadion
from users.models import User


class Bron(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='brons')
    stadion = models.ForeignKey(Stadion, on_delete=models.CASCADE, related_name='brons')
    hours = models.IntegerField()
    price = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    bron_time_start = models.DateTimeField()
    bron_time_end = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Rent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rents')
    stadion = models.ForeignKey(Stadion, on_delete=models.CASCADE, related_name='rents')
    hours = models.IntegerField()
    price = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    rent_time = models.DateTimeField()

    def __str__(self):
        return str(self.id)
