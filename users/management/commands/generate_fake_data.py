from django.core.management.base import BaseCommand
from users.models import User
from .generator_uzbek_phone_numbers import generate_uzbek_phone_number
from .generate_uzbek_names import generate_uzbek_names
from django.contrib.auth.hashers import make_password


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        print('Generate fake data for Users')
        password = make_password('856329471Jas')
        user_type = 'customer'

        for _ in range(20000):
            first_name = generate_uzbek_names()
            phone_number = generate_uzbek_phone_number()

            User.objects.create(
                first_name=first_name,
                password=password,
                type=user_type,
                phone_number=phone_number,
            )
