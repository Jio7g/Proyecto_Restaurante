# Proyecto Final - Restaurante

Programación web con Python, Django y JavaScript

Aplicación Django para pedidos de pizza y más. Permite a los usuarios registrarse/iniciar sesión y seleccionar elementos del menú desde una interfaz de usuario de JavaScript con cuadros contraídos para personalizaciones. La página de la cesta muestra los artículos actuales y permite una confirmación modal con los detalles del pago. La página de la cuenta muestra los pedidos actuales y anteriores de los usuarios en un formato conciso con la opción de mostrar detalles adicionales. Pueden filtrar sus pedidos utilizando el navegador lateral.

El sitio de administración se ha personalizado para mostrar información útil en cada página y la página de pedidos muestra los detalles del usuario. El contenido del pedido se ve yendo a la página de edición del pedido. Los tipos de pedidos separados (por ejemplo, pizOrders) están destinados al personal de cocina que puede ver una lista de todas las pizzas (u otros tipos de pedidos) y marcarlas como completadas. El propietario/administrador puede entonces marcar el pedido como listo para entrega o como completado. Ambas situaciones enviarán una notificación al usuario.

Utilicé la autenticación de Django para la página de registro, pero mejoré la experiencia del usuario usando JavaScript para que sepa si sus datos son válidos antes de enviarlos. El almacenamiento de datos de la cesta también utiliza JavaScript y variables de almacenamiento local que luego se pasan a Django en una solicitud posterior para el procesamiento de la base de datos.

El sistema de notificaciones se ha importado como una aplicación independiente a partir de un código fuente de terceros (django-notifications hq). Sin embargo, he modificado parte del código para que se ajuste a mi formato. Puede encontrar estos cambios enumerados a continuación:

********** added to 'notifications_tags.py' by Carlos Ramos **************************************************
in:
venv/
    notifications/
    ├── templatetags/
    │   └── notifications_tags.py
    ├── models.py
    ├── views.py
    ├── ...
**************************************************

def notifications_unread_list(context):
    user = user_context(context)
    if not user:
        return ''
    return user.notifications.unread()


if StrictVersion(get_version()) >= StrictVersion('2.0'):
    notifications_unread_list = register.simple_tag(takes_context=True)(
        notifications_unread_list)  # pylint: disable=invalid-name
else:
    notifications_unread_list = register.assignment_tag(takes_context=True)(notifications_unread_list)  # noqa

**********************************************************************