# Generated by Django 3.0.7 on 2020-06-06 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_auto_20200606_1117'),
    ]

    operations = [
        migrations.AddField(
            model_name='extras',
            name='price',
            field=models.DecimalField(decimal_places=2, default='00.50', max_digits=4),
        ),
    ]
