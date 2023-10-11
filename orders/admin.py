from django.contrib import admin
from django import forms

from notifications.signals import notify

from .models import *


def order_complete(modeladmin, request, queryset):
    # Admin Action Function - mark as completed
    user = request.user
    ident = request.POST['_selected_action']
    to = Orders.objects.get(order_id=ident)
    notify.send(user, recipient=to.user_id, verb='Your order is complete and has been archived!', action_object=to, level='success')
    queryset.update(active='N')


# Action description
order_complete.short_description = "Mark order as complete"


def order_delivery(modeladmin, request, queryset):
    # Admin Action Function - mark as out for delivery
    user = request.user
    ident = request.POST['_selected_action']
    to = Orders.objects.get(order_id=ident)
    notify.send(user, recipient=to.user_id, verb='Your order is out for delivery!',action_object=to, level='success')
    queryset.update(active='D')


# Action description
order_delivery.short_description = "Mark order as out for delivery"


def item_completed(modeladmin, request, queryset):
    # Admin Action Function - mark item as completed
    queryset.update(completed='Y')


# Action description
item_completed.short_description = "Mark item as completed"


class orderItemForm(forms.ModelForm):
    # filter pizItems select choices on change_form to show only those for the selected order
    def __init__(self, *args, **kwargs):
        super(orderItemForm, self).__init__(*args, **kwargs)
        self.fields['pizItems'].queryset = PizOrder.objects.filter(
            order_id=self.instance.order_id)
        self.fields['subItems'].queryset = SubOrder.objects.filter(
            order_id=self.instance.order_id)
        self.fields['pastaItems'].queryset = PastaOrder.objects.filter(
            order_id=self.instance.order_id)
        self.fields['saladItems'].queryset = SaladOrder.objects.filter(
            order_id=self.instance.order_id)
        self.fields['platItems'].queryset = PlatterOrder.objects.filter(
            order_id=self.instance.order_id)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'email', 'time_placed', 'cost')
    list_select_related = ['user_id']
    list_filter = ('active', )
    actions = (order_complete, order_delivery)
    form = orderItemForm

    def email(self, instance):
        return instance.user_id.email


class PizzaAdmin(admin.ModelAdmin):
    list_display = ('id', 'typ', 'category', 'smPrice', 'lgPrice', 'numTop')
    list_editable = ('smPrice', 'lgPrice', 'numTop')
    ordering = ('id',)


class PizItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'typ', 'size', 'custom_toppings', 'price')
    filter_horizontal = ('toppings',)
    list_filter = ('completed', )
    actions = (item_completed,)

    def order(self, instance):
        return instance.order_id


class SubAdmin(admin.ModelAdmin):
    list_display = ('id', 'typ', 'smPrice', 'lgPrice')
    list_editable = ('smPrice', 'lgPrice')
    ordering = ('id',)

class SubItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'typ', 'size', 'custom_extras', 'price')
    filter_horizontal = ('extras',)
    list_filter = ('completed', )
    actions = (item_completed,)

    def order(self, instance):
        return instance.order_id


class ExtraAdmin(admin.ModelAdmin):
    list_display = ('typ', 'price')
    list_editable = ['price']


class PastaAdmin(admin.ModelAdmin):
    list_display = ('id', 'typ', 'price')
    list_editable = ['price']
    ordering = ('id',)

class PastaItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'typ', 'price')
    list_filter = ('completed', )
    actions = (item_completed,)

    def order(self, instance):
        return instance.order_id


class SaladAdmin(admin.ModelAdmin):
    list_display = ('id', 'typ', 'price')
    list_editable = ['price']
    ordering = ('id',)

class SaladItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'typ', 'price')
    list_filter = ('completed', )
    actions = (item_completed,)

    def order(self, instance):
        return instance.order_id


class PlatterAdmin(admin.ModelAdmin):
    list_display = ('id', 'typ', 'smPrice', 'lgPrice')
    list_editable = ('smPrice', 'lgPrice')
    ordering = ('id',)

class PlatterItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'typ', 'size', 'price')
    list_filter = ('completed', )
    actions = (item_completed,)

    def order(self, instance):
        return instance.order_id


admin.site.register(Orders, OrderAdmin)
admin.site.register(Pizza, PizzaAdmin)
admin.site.register(Toppings)
admin.site.register(Sub, SubAdmin)
admin.site.register(Extras, ExtraAdmin)
admin.site.register(Pasta, PastaAdmin)
admin.site.register(Salad, SaladAdmin)
admin.site.register(Platter, PlatterAdmin)

admin.site.register(PizOrder, PizItemAdmin)
admin.site.register(SubOrder, SubItemAdmin)
admin.site.register(PastaOrder, PastaItemAdmin)
admin.site.register(SaladOrder, SaladItemAdmin)
admin.site.register(PlatterOrder, PlatterItemAdmin)

# admin.site.register(NotificationAdmin)

admin.site.site_header = "Pizza"
admin.site.site_title = "Pizza Admin"
admin.site.index_title = "Orders & Menu Administration"
