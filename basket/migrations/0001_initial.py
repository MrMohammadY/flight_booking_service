# Generated by Django 3.2 on 2022-01-25 14:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('flight', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='created time')),
                ('modified_time', models.DateTimeField(auto_now=True, verbose_name='modified time')),
                ('is_paid', models.BooleanField(default=False, verbose_name='is paid')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='carts', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'Cart',
                'verbose_name_plural': 'Carts',
                'db_table': 'cart',
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='created time')),
                ('modified_time', models.DateTimeField(auto_now=True, verbose_name='modified time')),
                ('first_name', models.CharField(max_length=50, verbose_name='first name')),
                ('last_name', models.CharField(max_length=60, verbose_name='last name')),
                ('national_code', models.CharField(max_length=10, verbose_name='national code')),
                ('birthday', models.DateField(verbose_name='birthday')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='basket.cart', verbose_name='cart')),
                ('flight', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='flight.flight', verbose_name='flight')),
                ('flight_seat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='flight.flightseat', verbose_name='flight seat')),
            ],
            options={
                'verbose_name': 'Ticket',
                'verbose_name_plural': 'Tickets',
                'db_table': 'ticket',
            },
        ),
    ]
