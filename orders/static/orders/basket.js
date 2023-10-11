document.addEventListener('DOMContentLoaded', () => {

    let bask = JSON.parse(localStorage.getItem('basket'));
    let basknum = document.querySelector('#basketnum');
    let div = document.querySelector('#basketList');

    if (bask == null) {
        div.innerHTML = '¡No tienes ningún artículo en tu cesta!';
        document.querySelector('#confirmOrder').disabled = true;
        document.querySelector('#deleteOrder').disabled = true;
        document.querySelector('#total').hidden = true;
    } else {

        let subtotal = localStorage.getItem('subtotal');
        document.querySelector('#subtotal').innerHTML = parseFloat(subtotal).toFixed(2);
        document.querySelector('#charge').innerHTML = parseFloat(subtotal).toFixed(2);

        for (i in bask) {

            let div = document.createElement("div");
            div.setAttribute('className', 'input-group');
            div.setAttribute('id', `item${i}`);
            div.setAttribute('name', `item${i}`);

            if (bask[i]['toppings'] == '') {
                // Crear plantilla
                const template1 = Handlebars.compile(document.querySelector('#basketItem1').innerHTML);

                // Agregar al DOM.
                const content = template1({
                    'ident': bask[i]['ident'],
                    'item': bask[i]['item'],
                    'type': bask[i]['type'],
                    'category': bask[i]['category'],
                    'size': bask[i]['size'],
                    'toppings': 'Sin ingredientes adicionales.',
                    'price': bask[i]['price']
                });

                document.querySelector('#basketList').innerHTML += content;

            } else {
                // Crear plantilla
                const template1 = Handlebars.compile(document.querySelector('#basketItem1').innerHTML);

                let toppings = '';

                for (k in bask[i]['toppings']) {
                    toppings += `${bask[i]['toppings'][k]}`;
                    if (k >= 0 && k < (bask[i]['toppings'].length - 1)) {
                        toppings += ', ';
                    }
                }

                // Agregar al DOM.
                const content = template1({
                    'ident': bask[i]['ident'],
                    'item': bask[i]['item'],
                    'type': bask[i]['type'],
                    'category': bask[i]['category'],
                    'size': bask[i]['size'],
                    'toppings': toppings,
                    'price': bask[i]['price']
                });

                document.querySelector('#basketList').innerHTML += content;
            }

        }
    }

    document.querySelector('#placeOrder').onclick = (button) => {

        document.querySelector('#hiddenData').value = localStorage.getItem('basket');
        document.querySelector('#hiddenSub').value = localStorage.getItem('subtotal');
        localStorage.removeItem('basket');
        localStorage.removeItem('subtotal');
        localStorage.removeItem('basknum');
        basknum.innerHTML = 0;
        basknum.hidden = true;
    };

    document.querySelector('#deleteOrder').onclick = (button) => {

        document.querySelector('#basketList').innerHTML = '¡No tienes ningún artículo en tu cesta!';
        localStorage.removeItem('basket');
        localStorage.removeItem('subtotal');
        localStorage.removeItem('basknum');
        basknum.innerHTML = 0;
        basknum.hidden = true;
        document.querySelector('#placeOrder').disabled = true;
        document.querySelector('#deleteOrder').disabled = true;
        document.querySelector('#confirmation').hidden = false;
        document.querySelector('#confirmation').innerHTML = '¡Se eliminaron con éxito todos los artículos de la cesta!';
    };

});
