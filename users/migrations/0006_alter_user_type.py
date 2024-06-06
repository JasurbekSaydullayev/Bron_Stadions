# Generated by Django 5.0.6 on 2024-06-06 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_user_phone_number_alter_user_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='type',
            field=models.CharField(choices=[('Admin', 'Admin'), ('customer', 'customer'), ('owner', 'owner')], default='customer', max_length=25),
        ),
    ]
