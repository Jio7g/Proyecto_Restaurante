
from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User


# orders
class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='orders')
    pizItems = models.ManyToManyField('PizOrder', blank=True, related_name='pizItems')
    subItems = models.ManyToManyField('SubOrder', blank=True, related_name='subItems')
    pastaItems = models.ManyToManyField('PastaOrder', blank=True, related_name='pastaItems')
    saladItems = models.ManyToManyField('SaladOrder', blank=True, related_name='saladItems')
    platItems = models.ManyToManyField('PlatterOrder', blank=True, related_name='platItems')
    time_placed = models.DateTimeField(auto_now_add=True)
    cost = models.DecimalField(max_digits=6, decimal_places=2, default=00.00)
    active = models.CharField(max_length=1, default='Y')

    class Meta:
        verbose_name = 'order'
        verbose_name_plural = 'orders'
    
    def __str__(self):
        return f"#{self.order_id} @ {self.time_placed.strftime('%x %X')}"


# pizza menu model to include regular and sicilian
class Pizza(models.Model):
    typ = models.CharField(max_length=10)
    category = models.CharField(max_length=10)
    smPrice = models.DecimalField(max_digits=4, decimal_places=2, default=00.00)
    lgPrice = models.DecimalField(max_digits=4, decimal_places=2, default=00.00)
    numTop = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.typ} - {self.category}"


# pizza orders
class PizOrder(models.Model):
    order_id = models.ForeignKey('Orders', on_delete=models.CASCADE, related_name='pizOrder')
    typ = models.ForeignKey(
        Pizza, on_delete=models.CASCADE, related_name='pizTyp')
    size = models.CharField(max_length=5)
    price = models.DecimalField(max_digits=4, decimal_places=2, default=00.00)
    toppings = models.ManyToManyField('Toppings', blank=True, related_name='customPiz')
    completed = models.CharField(max_length=1, default='N')
    
    def custom_toppings(self):
        return ", ".join([t.typ for t in self.toppings.all()])

    def __str__(self):
        return f"Type: {self.typ} || Size: {self.size} || Toppings: {self.custom_toppings()} || Price: ${self.price}"


# pizza toppings model
class Toppings(models.Model):
    typ = models.CharField(max_length=64)

    class Meta:
        verbose_name = 'topping'
        verbose_name_plural = 'toppings'

    def __str__(self):
        return f"{self.typ}"


# sub items
class Sub(models.Model):
    typ = models.CharField(max_length=64)
    smPrice = models.DecimalField(max_digits=4, decimal_places=2, default=00.00)
    lgPrice = models.DecimalField(max_digits=4, decimal_places=2, default=00.00)

    def __str__(self):
        return f"{self.typ}"

# sub orders
class SubOrder(models.Model):
    order_id = models.ForeignKey('Orders', on_delete=models.CASCADE, related_name='subOrders')
    typ = models.ForeignKey(
        Sub, on_delete=models.CASCADE, related_name='subTyp')
    size = models.CharField(max_length=5)
    price = models.DecimalField(max_digits=4, decimal_places=2, default=00.00)
    extras = models.ManyToManyField('Extras', related_name='subs')
    completed = models.CharField(max_length=1, default='N')

    def custom_extras(self):
        return ", ".join([t.typ for t in self.extras.all()])

    def __str__(self):
        return f"Type: {self.typ} || Size: {self.size} || Toppings: {self.custom_extras()} || Price: ${self.price}"


# extras for subs
class Extras(models.Model):
    typ = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=4, decimal_places=2, default='00.50')

    class Meta:
        verbose_name = 'extra'
        verbose_name_plural = 'extras'
    
    def __str__(self):
        return f"{self.typ}"


# pasta items
class Pasta(models.Model):
    typ = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.typ}"

# pasta orders
class PastaOrder(models.Model):
    order_id = models.ForeignKey('Orders', on_delete=models.CASCADE, related_name='pastaOrders')
    typ = models.ForeignKey(
        Pasta, on_delete=models.CASCADE, related_name='pastaTyp')
    price = models.DecimalField(max_digits=4, decimal_places=2, default=00.00)
    completed = models.CharField(max_length=1, default='N')

    def __str__(self):
        return f"{self.typ} -- ${self.price}"

# salad items
class Salad(models.Model):
    typ = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"Type: {self.typ}"

# salad orders
class SaladOrder(models.Model):
    order_id = models.ForeignKey('Orders', on_delete=models.CASCADE, related_name='saladOrders')
    typ = models.ForeignKey(
        Salad, on_delete=models.CASCADE, related_name='saladTyp')
    price = models.DecimalField(max_digits=4, decimal_places=2, default=00.00)
    completed = models.CharField(max_length=1, default='N')

    def __str__(self):
        return f"Type: {self.typ} || Price: ${self.price}"

# platter items
class Platter(models.Model):
    typ = models.CharField(max_length=64)
    smPrice = models.DecimalField(max_digits=4, decimal_places=2, default=00.00)
    lgPrice = models.DecimalField(max_digits=4, decimal_places=2, default=00.00)

    def __str__(self):
        return f"{self.typ} small = ${self.smPrice} large = ${self.lgPrice}"

# platter orders
class PlatterOrder(models.Model):
    order_id = models.ForeignKey('Orders', on_delete=models.CASCADE, related_name='platterOrders')
    typ = models.ForeignKey(
        Platter, on_delete=models.CASCADE, related_name='platterTyp')
    size = models.CharField(max_length=5)
    price = models.DecimalField(max_digits=4, decimal_places=2, default=00.00)
    completed = models.CharField(max_length=1, default='N')

    def __str__(self):
        return f"Type: {self.typ} || Size: {self.size} || Price: ${self.price}"