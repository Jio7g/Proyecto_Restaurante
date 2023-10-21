# Proyecto Final - Restaurante con Python, Django y JavaScript

## 🔧 Herramientas y lenguajes que se usaron:

![Python](https://img.shields.io/badge/-Python-05122A?style=flat&logo=python)&nbsp;
![Django](https://img.shields.io/badge/-Django-05122A?style=flat&logo=django&logoColor=092E20)&nbsp;
![JavaScript](https://img.shields.io/badge/-JavaScript-05122A?style=flat&logo=javascript)&nbsp;
![HTML](https://img.shields.io/badge/-HTML-05122A?style=flat&logo=HTML5)&nbsp;
![CSS](https://img.shields.io/badge/-CSS-05122A?style=flat&logo=CSS3&logoColor=1572B6)&nbsp;\
![Git](https://img.shields.io/badge/-Git-05122A?style=flat&logo=git)&nbsp;
![GitHub](https://img.shields.io/badge/-GitHub-05122A?style=flat&logo=github)&nbsp;
![Bootstrap](https://img.shields.io/badge/-Bootstrap-05122A?style=flat&logo=bootstrap&logoColor=563D7C)
![Visual Studio Code](https://img.shields.io/badge/-Visual%20Studio%20Code-05122A?style=flat&logo=visual-studio-code&logoColor=007ACC)&nbsp;

##

Aplicación Django para pedidos de un restaurante y más. Permite a los usuarios registrarse/iniciar sesión y seleccionar elementos del menú desde una interfaz de usuario de JavaScript con cuadros contraídos para personalizaciones. La página de la cesta/carrito muestra los artículos actuales y permite una confirmación modal con los detalles del pago. La página de la cuenta muestra los pedidos actuales y anteriores de los usuarios en un formato conciso con la opción de mostrar detalles adicionales. Pueden filtrar sus pedidos utilizando el navegador lateral.

El sitio de administración se ha personalizado para mostrar información útil en cada página y la página de pedidos muestra los detalles del usuario. El contenido del pedido se ve yendo a la página de edición del pedido. Los tipos de pedidos separados (por ejemplo, pizOrders) están destinados al personal de cocina que puede ver una lista de todas las pizzas (u otros tipos de pedidos) y marcarlas como completadas. El propietario/administrador puede entonces marcar el pedido como listo para entrega o como completado. Ambas situaciones enviarán una notificación al usuario.

Utilicé la autenticación de Django para la página de registro, pero mejoré la experiencia del usuario usando JavaScript para que sepa si sus datos son válidos antes de enviarlos. El almacenamiento de datos de la cesta también utiliza JavaScript y variables de almacenamiento local que luego se pasan a Django en una solicitud posterior para el procesamiento de la base de datos.

El sistema de notificaciones se ha importado como una aplicación independiente a partir de un código fuente de terceros (django-notifications hq). Sin embargo, modificamos parte del código para que se ajuste a mi formato. Se Pueden encontrar estos cambios enumerados a continuación:

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


## Home:

![home1](https://github.com/Jio7g/Pruebas_Proyecto_Restaurante/assets/142697112/97898bc1-130a-4cdc-b7fd-00fcdd3861be)

![home2](https://github.com/Jio7g/Pruebas_Proyecto_Restaurante/assets/142697112/c513723a-d15f-4830-ae05-e0cf1914b312)

![home3](https://github.com/Jio7g/Pruebas_Proyecto_Restaurante/assets/142697112/50659d93-81a2-4f6b-a317-0e9dbe6c05ce)

![home4](https://github.com/Jio7g/Pruebas_Proyecto_Restaurante/assets/142697112/4db03014-e850-4f8a-bb91-075e88e03dc0)

![home5](https://github.com/Jio7g/Pruebas_Proyecto_Restaurante/assets/142697112/4cb53a53-7a09-4195-9270-c12612b660a1)

## Menu:

![menu](https://github.com/Jio7g/Pruebas_Proyecto_Restaurante/assets/142697112/d174afc3-1f55-4229-b760-cd38f7329110)

## Direccion:

![direccion](https://github.com/Jio7g/Pruebas_Proyecto_Restaurante/assets/142697112/aa7657fe-35ab-442b-8b63-2dcbc45a623d)

## Historial de Ordenes:

![historia-ordenes](https://github.com/Jio7g/Pruebas_Proyecto_Restaurante/assets/142697112/d8203a41-57bf-4e81-9acf-500c41991bba)

## Login:

![inicio-sesion](https://github.com/Jio7g/Pruebas_Proyecto_Restaurante/assets/142697112/329f58db-f6fb-4cc6-bed7-c5d478fcc252)

## Register:

![registro](https://github.com/Jio7g/Pruebas_Proyecto_Restaurante/assets/142697112/2b02e577-1a72-4109-ac98-031585467250)
