# Generated by Django 3.0.7 on 2020-06-09 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_auto_20200609_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='pastaItems',
            field=models.ManyToManyField(blank=True, related_name='pastaItems', to='orders.PastaOrder'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='platItems',
            field=models.ManyToManyField(blank=True, related_name='platItems', to='orders.PlatterOrder'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='saladItems',
            field=models.ManyToManyField(blank=True, related_name='saladItems', to='orders.SaladOrder'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='subItems',
            field=models.ManyToManyField(blank=True, related_name='subItems', to='orders.SubOrder'),
        ),
    ]
