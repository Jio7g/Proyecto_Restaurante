from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import RegForm
from notifications.signals import notify
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
import json
# from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


def home(request):
    return render(request, 'orders/index.html')

def register(request):
    if request.method == 'POST':
        form = RegForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            try:    
                    auto = User.objects.get(username='AutomaticSystemMessage')
                    notify.send(auto, recipient=user, verb="¡Bienvenido! Gracias por registrarte en nuestro Restaurante. Esperamos que encuentres algo que te guste y esperamos recibir un pedido tuyo muy pronto. Visita nuestra página de 'menú' para agregar elementos a tu carrito. Puedes ver tus pedidos en tu página de 'cuenta'.", level='info')
                    return HttpResponseRedirect(reverse("orders:menu"))
            
            except ObjectDoesNotExist:
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
            return render(request, "orders/login.html", {"message": "usuario/contraseña incorrecta."})
    else:
        logout(request)
        return render(request, 'orders/login.html')

def log_out(request):
    logout(request)
    return render(request, 'orders/login.html', {'success': '¡Cerró sesión exitosamente!'})

def menu(request):
    if request.method == 'GET':
        user = request.user
        it = Pizza.objects.all()
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
            payment_option = request.POST.get('payment_option')
            cardnum = "" 
            
            if payment_option == 'cashPayment':  # Pago en Efectivo
                # Procesa la compra para pago en efectivo
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
                    elif row['item'] == 'sub':
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
                        ord1.cost = total_cost
                        ord1.save()
                    else:
                        continue
                auto = User.objects.get(username='AutomaticSystemMessage')
                notify.send(auto, recipient=user, verb="¡Sus datos de pago han sido confirmados y su pedido se ha realizado correctamente! Te avisaremos cuando esté disponible para entrega.", action_object=ord1, level='success')
                return HttpResponseRedirect(reverse("orders:account"))
            
            elif payment_option == 'cardOnDelivery':  # Pago con Tarjeta contra Entrega
                # Procesa la compra para pago con tarjeta contra entrega
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
                    elif row['item'] == 'sub':
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
                notify.send(auto, recipient=user, verb="¡Su pedido se ha realizado correctamente! Te avisaremos cuando esté disponible para entrega.", action_object=ord1, level='success')
                return HttpResponseRedirect(reverse("orders:account"))
            
            elif payment_option == 'onlinePayment':  # Pago en Línea
                 # validador de tarjetas ****************************
             if len(cardnum) < 13 or len(cardnum) > 16 or len(cardnum) == 14:
                messages.add_message(
                    request, messages.ERROR, 'Tarjeta no válida 1 - transacción fallida.')
                return HttpResponseRedirect(reverse("orders:basket"))
            else:
                length = len(cardnum)
                # paso 1 calcula 2x cada dos números y luego suma
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

                # paso 2 calcula la suma de los dígitos restantes
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

                # paso 3 comprobar que termina en 0 y asignar tipo de tarjeta
                end = int(total) % 10

                if not end == 0:
                    messages.add_message(
                        request, messages.ERROR, 'Tarjeta no válida 2 - transacción fallida.')
                    return HttpResponseRedirect(reverse("orders:basket"))
                elif length == 15:
                    if cardnum[0] == '3' and cardnum[1] == '4' or '7':
                        pass
                    else:
                        messages.add_message(
                            request, messages.ERROR, 'Tarjeta no válida 3 - transacción fallida.')
                        return HttpResponseRedirect(reverse("orders:basket"))

                elif length == 16:
                    if cardnum[0] == '5' and 0 < int(cardnum[1]) < 6:
                        pass
                    elif cardnum[0] == '4':
                        pass
                    else:
                        messages.add_message(
                            request, messages.ERROR, 'Tarjeta no válida 4 - transacción fallida.')
                        return HttpResponseRedirect(reverse("orders:basket"))

                elif length == 13:
                    if cardnum[0] == '4':
                        pass
                    else:
                        messages.add_message(
                            request, messages.ERROR, 'Tarjeta no válida 5 - transacción fallida.')
                        return HttpResponseRedirect(reverse("orders:basket"))
            # fin del validador de tarjetas ****************************
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
                    elif row['item'] == 'sub':
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
                notify.send(auto, recipient=user, verb="¡Sus datos de pago han sido confirmados y su pedido se ha realizado correctamente! Te avisaremos cuando esté disponible para entrega.", action_object=ord1, level='success')
                return HttpResponseRedirect(reverse("orders:account"))
        else:
                # Opción de pago no válida
                return HttpResponseRedirect(reverse("orders:basket"))    
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

def directions(request):
        return render(request, "orders/directions.html")

def contact(request):
        return render(request, "orders/contact.html")

def page_not_found_404(request, exception):
        return render(request, "orders/404.html")