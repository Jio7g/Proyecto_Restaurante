# Generated by Django 3.0.7 on 2020-06-06 10:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_basket'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pizorder',
            name='category',
        ),
        migrations.RemoveField(
            model_name='platter',
            name='price',
        ),
        migrations.RemoveField(
            model_name='platter',
            name='size',
        ),
        migrations.RemoveField(
            model_name='sub',
            name='extras',
        ),
        migrations.RemoveField(
            model_name='sub',
            name='size',
        ),
        migrations.AddField(
            model_name='platter',
            name='lgPrice',
            field=models.DecimalField(decimal_places=2, default='00.00', max_digits=4),
        ),
        migrations.AddField(
            model_name='platter',
            name='smPrice',
            field=models.DecimalField(decimal_places=2, default='00.00', max_digits=4),
        ),
        migrations.AddField(
            model_name='sub',
            name='lgPrice',
            field=models.DecimalField(decimal_places=2, default='00.00', max_digits=4),
        ),
        migrations.AddField(
            model_name='sub',
            name='smPrice',
            field=models.DecimalField(decimal_places=2, default='00.00', max_digits=4),
        ),
        migrations.AlterField(
            model_name='pizorder',
            name='typ',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pizTyp', to='orders.Pizza'),
        ),
        migrations.CreateModel(
            name='SubOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=5)),
                ('price', models.DecimalField(decimal_places=2, default='00.00', max_digits=4)),
                ('extras', models.ManyToManyField(related_name='subs', to='orders.Extras')),
                ('order_id', models.ManyToManyField(related_name='subOrders', to='orders.Orders')),
                ('typ', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subTyp', to='orders.Sub')),
            ],
        ),
        migrations.CreateModel(
            name='SaladOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, default='00.00', max_digits=4)),
                ('order_id', models.ManyToManyField(related_name='saladOrders', to='orders.Orders')),
                ('typ', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saladTyp', to='orders.Salad')),
            ],
        ),
        migrations.CreateModel(
            name='PlatterOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=5)),
                ('price', models.DecimalField(decimal_places=2, default='00.00', max_digits=4)),
                ('order_id', models.ManyToManyField(related_name='platterOrders', to='orders.Orders')),
                ('typ', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='platterTyp', to='orders.Platter')),
            ],
        ),
        migrations.CreateModel(
            name='PastaOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, default='00.00', max_digits=4)),
                ('order_id', models.ManyToManyField(related_name='pastaOrders', to='orders.Orders')),
                ('typ', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pastaTyp', to='orders.Pasta')),
            ],
        ),
    ]
