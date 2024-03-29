# Generated by Django 3.2 on 2022-01-25 16:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basket', '0001_initial'),
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='cart',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='invoice', to='basket.cart', verbose_name='cart'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='uuid',
            field=models.CharField(default='3fef1ff6b70d46b093eb762c74a2bf3d', max_length=32, unique=True, verbose_name='uuid'),
        ),
    ]
