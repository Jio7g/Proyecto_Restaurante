from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import RegForm
from notifications.signals import notify
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required


import json


def home(request):
    return render(request, 'orders/home.html')


def register(request):

    if request.method == 'POST':

        form = RegForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)

            login(request, user)

            auto = User.objects.get(username='AutomaticSystemMessage')
            notify.send(auto, recipient=user, verb="Welcome! Thank you for signing up to Pizza. We hope you find something that makes your mouth water and we look forward to receiving an order from you very soon. Check out our 'menu' page to add things to your basket. You can view orders you have placed in your 'account' page.", level='info')

            return HttpResponseRedirect(reverse("orders:menu"))

        else:
            messages.error(request, form.errors)
            return render(request, 'orders/register.html')

    else:
        return render(request, 'orders/register.html')


def log_in(request):

    if request.method == 'POST':

        username = request.POST["un"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("orders:menu"))
        else:
            return render(request, "users/login.html", {"message": "Invalid username/password."})

    else:
        logout(request)
        return render(request, 'orders/login.html')


def log_out(request):

    logout(request)
    return render(request, 'orders/login.html', {'success': 'Successfully logged out!'})

# @login_required
from django.shortcuts import render
from .models import *

def menu(request):
    if request.method == 'GET':
        user = request.user

        # django won't allow range in template {% %} of html page hence defining it here
        it = Pizza.objects.all()

        # iterate over pizas and add column for ranges
        for row in it:
            num = row.numTop
            row.num = range(1, (num+1))

        context = {
            "user": user,
            "pizza": it,
            "toppings": Toppings.objects.all(),
            "subs": Sub.objects.all(),
            "extras": Extras.objects.all(),
            "pasta": Pasta.objects.all(),
            "salads": Salad.objects.all(),
            "platters": Platter.objects.all(),
        }
        return render(request, "orders/menu.html", context)



def place(request):

    if request.user.is_authenticated:

        if request.method == 'POST':

            user = request.user
            data = request.POST['hiddenData']
            data = json.loads(data)

            cardnum = request.POST['cardNumber']

            # card validator ****************************
            if len(cardnum) < 13 or len(cardnum) > 16 or len(cardnum) == 14:
                messages.add_message(
                    request, messages.ERROR, 'Card Invalid 1 - Transaction unsuccessful.')
                return HttpResponseRedirect(reverse("orders:basket"))
            else:
                length = len(cardnum)
                # step 1 calculate 2x every other number then add
                i = length - 2
                sum1 = 0
                sum2 = 0
                end = 1
                while i >= 0:
                    val = int(cardnum[i]) * 2

                    if val >= 10:
                        val1 = []
                        for k in range(2):
                            val1.append(int(val) % 10)
                            val = val / 10
                            sum1 += val1[k]
                    else:
                        sum1 += val

                    i -= 2

                # step 2 calculate sum of digits remaining
                i = length - 1
                while i >= 0:
                    val = int(cardnum[i])

                    if val >= 10:
                        val1 = []
                        for k in range(2):
                            val1.append(int(val) % 10)
                            val = val / 10
                            sum2 += val1[k]
                    else:
                        sum2 += val

                    i -= 2

                total = sum1 + sum2

                # step 3 check ending in 0 and assign card type
                end = int(total) % 10

                if not end == 0:
                    messages.add_message(
                        request, messages.ERROR, 'Card Invalid 2 - Transaction unsuccessful.')
                    return HttpResponseRedirect(reverse("orders:basket"))
                elif length == 15:
                    if cardnum[0] == '3' and cardnum[1] == '4' or '7':
                        pass
                    else:
                        messages.add_message(
                            request, messages.ERROR, 'Card Invalid 3 - Transaction unsuccessful.')
                        return HttpResponseRedirect(reverse("orders:basket"))

                elif length == 16:
                    if cardnum[0] == '5' and 0 < int(cardnum[1]) < 6:
                        pass
                    elif cardnum[0] == '4':
                        pass
                    else:
                        messages.add_message(
                            request, messages.ERROR, 'Card Invalid 4 - Transaction unsuccessful.')
                        return HttpResponseRedirect(reverse("orders:basket"))

                elif length == 13:
                    if cardnum[0] == '4':
                        pass
                    else:
                        messages.add_message(
                            request, messages.ERROR, 'Card Invalid 5 - Transaction unsuccessful.')
                        return HttpResponseRedirect(reverse("orders:basket"))
            # end of card validator ****************************

            ord1 = Orders(user_id=user)
            ord1.save()

            for row in data:
                if row['item'] == 'Pizza':
                    p1 = Pizza.objects.get(id=row['ident'])

                    po1 = PizOrder(order_id=ord1, typ=p1, price=float(row['price']), size=row['size'])

                    po1.save()

                    if row['toppings'] != []:
                        for row in row['toppings']:
                            top = Toppings.objects.get(
                                typ=row.replace('&amp;', '&'))
                            po1.toppings.add(top)
                            po1.save()

                    ord1.cost += po1.price
                    ord1.pizItems.add(po1)
                    ord1.save()

                elif row['item'] == 'Sub':
                    s1 = Sub.objects.get(id=row['ident'])

                    so1 = SubOrder(order_id=ord1,
                                   typ=s1, price=float(row['price']), size=row['size'])
                    so1.save()

                    if row['toppings'] != []:
                        for row in row['toppings']:
                            row = Extras.objects.get(
                                typ=row.replace('&amp;', '&'))
                            so1.extras.add(row)
                            so1.save()

                    ord1.cost += so1.price
                    ord1.subItems.add(so1)
                    ord1.save()

                elif row['item'] == 'Pasta':
                    pasta1 = Pasta.objects.get(id=row['ident'])

                    paO1 = PastaOrder(order_id=ord1,
                                      typ=pasta1, price=float(row['price']))
                    paO1.save()

                    ord1.cost += paO1.price
                    ord1.pastaItems.add(paO1)
                    ord1.save()

                elif row['item'] == 'Salad':
                    salad1 = Salad.objects.get(id=row['ident'])

                    salO1 = SaladOrder(order_id=ord1,
                                       typ=salad1, price=float(row['price']))
                    salO1.save()

                    ord1.cost += salO1.price
                    ord1.saladItems.add(salO1)
                    ord1.save()

                elif row['item'] == 'Platter':
                    platter1 = Platter.objects.get(id=row['ident'])

                    plato1 = PlatterOrder(order_id=ord1,
                                          typ=platter1, price=float(row['price']), size=row['size'])
                    plato1.save()

                    ord1.cost += plato1.price
                    ord1.platItems.add(plato1)
                    ord1.save()

                else:
                    continue

            auto = User.objects.get(username='AutomaticSystemMessage')
            notify.send(auto, recipient=user, verb="Your payment details have been confirmed and your order has been placed successfully! We'll notify you when it's out for delivery.", action_object=ord1, level='success')

            return HttpResponseRedirect(reverse("orders:account"))

    else:
        return HttpResponseRedirect(reverse("orders:login"))


def basket(request):

    user = request.user

    context = {
        "user": user
    }

    return render(request, 'orders/basket.html', context)


def filter(request, filter_by):

    if filter_by == 'newest':

        user = request.user

        active = Orders.objects.filter(
            user_id=user, active='Y').order_by('-time_placed')
        delivery = Orders.objects.filter(
            user_id=user, active='D').order_by('-time_placed')
        expired = Orders.objects.filter(
            user_id=user, active='N').order_by('-time_placed')

        pizzas = PizOrder.objects.all()
        subs = SubOrder.objects.all()
        pastas = PastaOrder.objects.all()
        salads = SaladOrder.objects.all()
        platters = PlatterOrder.objects.all()

        context = {
            "user": user,
            "active": active,
            "delivery": delivery,
            "expired": expired,
            "pizzas": pizzas,
            "subs": subs,
            "pastas": pastas,
            "salads": salads,
            "platters": platters
        }

        return render(request, 'orders/account.html', context)

    elif filter_by == 'oldest':

        user = request.user

        active = Orders.objects.filter(
            user_id=user, active='Y').order_by('time_placed')
        delivery = Orders.objects.filter(
            user_id=user, active='D').order_by('time_placed')
        expired = Orders.objects.filter(
            user_id=user, active='N').order_by('time_placed')

        pizzas = PizOrder.objects.all()
        subs = SubOrder.objects.all()
        pastas = PastaOrder.objects.all()
        salads = SaladOrder.objects.all()
        platters = PlatterOrder.objects.all()

        context = {
            "user": user,
            "active": active,
            "delivery": delivery,
            "expired": expired,
            "pizzas": pizzas,
            "subs": subs,
            "pastas": pastas,
            "salads": salads,
            "platters": platters
        }

        return render(request, 'orders/account.html', context)

    elif filter_by == 'cheapest':

        user = request.user

        active = Orders.objects.filter(
            user_id=user, active='Y').order_by('cost')
        delivery = Orders.objects.filter(
            user_id=user, active='D').order_by('cost')
        expired = Orders.objects.filter(
            user_id=user, active='N').order_by('cost')

        pizzas = PizOrder.objects.all()
        subs = SubOrder.objects.all()
        pastas = PastaOrder.objects.all()
        salads = SaladOrder.objects.all()
        platters = PlatterOrder.objects.all()

        context = {
            "user": user,
            "active": active,
            "delivery": delivery,
            "expired": expired,
            "pizzas": pizzas,
            "subs": subs,
            "pastas": pastas,
            "salads": salads,
            "platters": platters
        }

        return render(request, 'orders/account.html', context)

    elif filter_by == 'expensive':
        user = request.user

        active = Orders.objects.filter(
            user_id=user, active='Y').order_by('-cost')
        delivery = Orders.objects.filter(
            user_id=user, active='D').order_by('-cost')
        expired = Orders.objects.filter(
            user_id=user, active='N').order_by('-cost')

        pizzas = PizOrder.objects.all()
        subs = SubOrder.objects.all()
        pastas = PastaOrder.objects.all()
        salads = SaladOrder.objects.all()
        platters = PlatterOrder.objects.all()

        context = {
            "user": user,
            "active": active,
            "delivery": delivery,
            "expired": expired,
            "pizzas": pizzas,
            "subs": subs,
            "pastas": pastas,
            "salads": salads,
            "platters": platters
        }

        return render(request, 'orders/account.html', context)

    elif filter_by == 'cheapest':

        user = request.user

        active = Orders.objects.filter(
            user_id=user, active='Y').order_by('cost')
        delivery = Orders.objects.filter(
            user_id=user, active='D').order_by('cost')
        expired = Orders.objects.filter(
            user_id=user, active='N').order_by('cost')

        pizzas = PizOrder.objects.all()
        subs = SubOrder.objects.all()
        pastas = PastaOrder.objects.all()
        salads = SaladOrder.objects.all()
        platters = PlatterOrder.objects.all()

        context = {
            "user": user,
            "active": active,
            "delivery": delivery,
            "expired": expired,
            "pizzas": pizzas,
            "subs": subs,
            "pastas": pastas,
            "salads": salads,
            "platters": platters
        }

        return render(request, 'orders/account.html', context)

    elif filter_by == 'active':

        user = request.user

        active = Orders.objects.filter(
            user_id=user, active='Y').order_by('-time_placed')

        pizzas = PizOrder.objects.all()
        subs = SubOrder.objects.all()
        pastas = PastaOrder.objects.all()
        salads = SaladOrder.objects.all()
        platters = PlatterOrder.objects.all()

        context = {
            "user": user,
            "active": active,
            "pizzas": pizzas,
            "subs": subs,
            "pastas": pastas,
            "salads": salads,
            "platters": platters
        }

        return render(request, 'orders/account.html', context)

    elif filter_by == 'delivery':

        user = request.user

        delivery = Orders.objects.filter(
            user_id=user, active='D').order_by('-time_placed')

        pizzas = PizOrder.objects.all()
        subs = SubOrder.objects.all()
        pastas = PastaOrder.objects.all()
        salads = SaladOrder.objects.all()
        platters = PlatterOrder.objects.all()

        context = {
            "user": user,
            "delivery": delivery,
            "pizzas": pizzas,
            "subs": subs,
            "pastas": pastas,
            "salads": salads,
            "platters": platters
        }

        return render(request, 'orders/account.html', context)

    else:

        user = request.user

        expired = Orders.objects.filter(
            user_id=user, active='N').order_by('-time_placed')

        pizzas = PizOrder.objects.all()
        subs = SubOrder.objects.all()
        pastas = PastaOrder.objects.all()
        salads = SaladOrder.objects.all()
        platters = PlatterOrder.objects.all()

        context = {
            "user": user,
            "expired": expired,
            "pizzas": pizzas,
            "subs": subs,
            "pastas": pastas,
            "salads": salads,
            "platters": platters
        }

        return render(request, 'orders/account.html', context)


def account(request):

    user = request.user

    active = Orders.objects.filter(
        user_id=user, active='Y').order_by('-time_placed')
    delivery = Orders.objects.filter(
        user_id=user, active='D').order_by('-time_placed')
    expired = Orders.objects.filter(
        user_id=user, active='N').order_by('-time_placed')

    pizzas = PizOrder.objects.all()
    subs = SubOrder.objects.all()
    pastas = PastaOrder.objects.all()
    salads = SaladOrder.objects.all()
    platters = PlatterOrder.objects.all()

    context = {
        "user": user,
        "active": active,
        "delivery": delivery,
        "expired": expired,
        "pizzas": pizzas,
        "subs": subs,
        "pastas": pastas,
        "salads": salads,
        "platters": platters
    }

    return render(request, 'orders/account.html', context)


@user_passes_test(lambda u: u.is_staff)
def user_orders(request):
    if request.user.is_staff:
        orders = Orders.objects.all().order_by('-time_placed')  # Un admin verá todas las órdenes
    else:
        return redirect('orders/menu.html')  # Redirige a los no administradores a alguna otra vista

    return render(request, 'orders/user_orders.html', {'orders': orders})