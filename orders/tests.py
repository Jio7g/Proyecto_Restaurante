from django.test import TestCase

from django.contrib.auth.models import User
from orders.models import *

# Create your tests here.
class ModelsTestCase(TestCase):

    def setUp(self):

        # create users
        u1 = User.objects.create(username="test1", email="test1@example.com", password="test1pw")
        u2 = User.objects.create(username="test2", email="test2@example.com", password="test2pw")

        # Create pizzas
        p1 = Pizza.objects.create(typ='Regular', category='Cheese', smPrice='12.70', lgPrice='17.95', numTop='0')
        p2 = Pizza.objects.create(typ='Regular', category='1 topping', smPrice='13.70', lgPrice='19.95', numTop='1')
        p3 = Pizza.objects.create(typ='Regular', category='2 topping', smPrice='15.20', lgPrice='21.95', numTop='2')
        p4 = Pizza.objects.create(typ='Regular', category='3 topping', smPrice='16.20', lgPrice='23.95', numTop='3')
        p5 = Pizza.objects.create(typ='Sicilian', category='3 item', smPrice='29.45', lgPrice='44.70', numTop='3')

        # Create toppings
        Pepperoni = Toppings.objects.create(typ='Pepperoni')
        Sausage = Toppings.objects.create(typ='Sausage')
        Mushrooms = Toppings.objects.create(typ='Mushrooms')
        Onions = Toppings.objects.create(typ='Onions')
        Ham = Toppings.objects.create(typ='Ham')
        CanadianBacon = Toppings.objects.create(typ='Canadian Bacon')
        Pineapple = Toppings.objects.create(typ='Pineapple')
        
        # Create orders
        ord1 = Orders.objects.create(user_id=u1)
        ord2 = Orders.objects.create(user_id=u2)
        ord3 = Orders.objects.create(user_id=u2, active="N")

    
    def test_order_id(self):
        """check auto id for orders"""

        u1 = User.objects.get(id='1')
        u2 = User.objects.get(id='2')

        ord1 = Orders.objects.get(user_id=u1)
        ord2 = Orders.objects.get(user_id=u2, active='Y')
        ord3 = Orders.objects.get(user_id=u2, active="N")

        ord4 = Orders(user_id=u1)
        ord4.save()

        self.assertFalse(ord1.order_id == None)
        self.assertFalse(ord2.order_id == None)
        self.assertFalse(ord3.order_id == None)
        self.assertFalse(ord4.order_id == None)
        self.assertFalse(ord1.pk == None)
        self.assertFalse(ord2.pk == None)
        self.assertFalse(ord3.pk == None)
        self.assertFalse(ord4.pk == None)


    def test_price_query(self):
        """check price for pizzas"""
        p1 = Pizza.objects.get(typ='Regular', category='Cheese')
        p2 = Pizza.objects.get(typ='Regular', category='1 topping')
        p3 = Pizza.objects.get(typ='Sicilian', category='3 item')
        self.assertEqual(float(p1.smPrice), 12.70)
        self.assertEqual(float(p1.lgPrice), 17.95)
        self.assertEqual(float(p2.smPrice), 13.70)
        self.assertEqual(float(p2.lgPrice), 19.95)
        self.assertEqual(float(p3.smPrice), 29.45)
        self.assertEqual(float(p3.lgPrice), 44.70)
    
    def test_order_exists(self):
        """check order exists"""

        u1 = User.objects.get(id='1')
        u2 = User.objects.get(id='2')
        
        ord1 = Orders.objects.get(order_id='1')
        ord2 = Orders.objects.get(order_id='2')
        ord3 = Orders.objects.all()

        count = 0

        for row in ord3:
            if row.active == 'Y':
                count += 1

        self.assertEqual(ord1.user_id, u1)
        self.assertEqual(ord2.order_id, 2)
        self.assertEqual(count, 2)

    
    def test_add_pizItem1(self):
        """create a simple pizza order"""

        u1 = User.objects.get(id='1')

        ord1 = Orders.objects.get(user_id=u1, active='Y')

        p1 = Pizza.objects.get(typ='Regular', category='Cheese')
        p2 = Pizza.objects.get(typ='Regular', category='1 topping')

        pepperoni = Toppings.objects.get(typ='Pepperoni')

        po1 = PizOrder.objects.create(typ=p1, price=p1.lgPrice, size='large')
        po1.order_id.add(ord1)
        po1.save()
        ord1.cost = po1.price
        ord1.save()

        po2 = PizOrder.objects.create(typ=p2, price=p2.smPrice, size='small')
        po2.order_id.add(ord1)
        po2.save()

        po3 = PizOrder.objects.create(typ=p2, price=p2.smPrice, size='small')
        po3.order_id.add(ord1)
        po3.toppings.add(pepperoni)
        po3.save()

        self.assertEqual(float(po1.price), 17.95)
        self.assertEqual(po1.price, ord1.cost)
        self.assertEqual(po1.toppings.count(), 0)
        self.assertEqual(po1.toppings.count(), p1.numTop)
        self.assertFalse(po2.toppings.count(), p2.numTop)
        self.assertFalse(po2 == po3)

    
    def test_add_pizOrder(self):
        """create a complex pizza order with multiple pizzas"""

        u1 = User.objects.get(id='1')
        u2 = User.objects.get(id='2')

        ord1 = Orders.objects.get(user_id=u1, active='Y')
        ord2 = Orders.objects.get(user_id=u2, active='Y')

        p1 = Pizza.objects.get(typ='Regular', category='Cheese')
        p2 = Pizza.objects.get(typ='Regular', category='1 topping')
        p3 = Pizza.objects.get(typ='Regular', category='2 topping')
        p4 = Pizza.objects.get(typ='Sicilian', category='3 item')

        pepperoni = Toppings.objects.get(typ='Pepperoni')
        ham = Toppings.objects.get(typ='Ham')
        sausage = Toppings.objects.get(typ='Sausage')
        mushrooms = Toppings.objects.get(typ='Mushrooms')
        onions = Toppings.objects.get(typ='Onions')

        # ------------------- first order -----------------------

        # order 1 - cheese pizza
        po1 = PizOrder.objects.create(typ=p1, price=p1.lgPrice, size='large')
        po1.order_id.add(ord1)
        po1.save()
        ord1.cost += po1.price
        ord1.save()

        # order 1 - 1 topping
        po2 = PizOrder.objects.create(typ=p2, price=p2.smPrice, size='small')
        po2.order_id.add(ord1)
        po2.toppings.add(pepperoni)
        po2.save()
        ord1.cost += po2.price
        ord1.save()

        ord1.pizItems.add(po1, po2)
        ord1.save()

        # ---------------- second order ------------------------

        # order 2 - 1 topping
        po3 = PizOrder.objects.create(typ=p2, price=p2.lgPrice, size='large')
        po3.order_id.add(ord2)
        po3.toppings.add(pepperoni)
        po3.save()
        ord2.cost += po3.price
        ord2.save()

        # order 2 - 2 toppings
        po4 = PizOrder.objects.create(typ=p3, price=p3.lgPrice, size='large')
        po4.order_id.add(ord2)
        po4.toppings.add(pepperoni, sausage)
        po4.save()
        ord2.cost += po4.price
        ord2.save()

        # order 2 - 2 toppings again
        po5 = PizOrder.objects.create(typ=p3, price=p3.smPrice, size='small')
        po5.order_id.add(ord2)
        po5.toppings.add(pepperoni, sausage)
        po5.save()
        ord2.cost += po5.price
        ord2.save()

        # order 2 - Sicilian 3 toppings
        po6 = PizOrder.objects.create(typ=p4, price=p4.smPrice, size='small')
        po6.order_id.add(ord2)
        po6.toppings.add(ham, mushrooms, onions)
        po6.save()
        ord2.cost += po6.price
        ord2.save()

        ord2.pizItems.add(po3, po4, po5, po6)
        ord2.save()

        # order 1
        order1tot = po1.price + po2.price
        # order 2
        order2tot = po3.price + po4.price + po5.price + po6.price

        ordCount = Orders.objects.filter(user_id=u2, active='Y').count()

        self.assertEqual(ord1.pizItems.count(), 2)
        self.assertEqual(ord2.pizItems.count(), 4)
        
        self.assertEqual(ord1.cost, order1tot)
        self.assertEqual(ord2.cost, order2tot)

        self.assertEqual(ordCount, 1)
    