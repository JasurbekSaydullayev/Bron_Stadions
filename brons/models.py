from django.db import models

from stadions.models import Stadion
from users.models import User

bron_status_choices = (
    ('Yangi', 'Yangi'),
    ('Tasdiqlangan', 'Tasdiqlangan'),
    ('Cancel from Owner', "Bron maydon egasi tomonidan bekor qilingan"),
    ('Cancel from Customer', 'Bron buyurtmachi tomonidan bekor qilingan')
)


class Bron(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='brons')
    stadion = models.ForeignKey(Stadion, on_delete=models.CASCADE, related_name='brons')
    hours = models.IntegerField()
    price_for_hour = models.BigIntegerField()
    full_price = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    bron_time_start = models.DateTimeField()
    bron_time_end = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    is_confirmed = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=bron_status_choices, default='Yangi')

    def __str__(self):
        return str(self.id)