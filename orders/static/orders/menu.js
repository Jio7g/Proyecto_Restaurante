document.addEventListener('DOMContentLoaded', () => {
    // Obtener el elemento del contador del carrito
    let basknum = document.querySelector('#basketnum');
    let basketnum = JSON.parse(localStorage.getItem('basknum'));

    // Actualizar el contador del carrito si es mayor que 0
    if (basketnum > 0) {
        basknum.innerHTML = basketnum;
        basknum.hidden = false;
    } else {
        basknum.innerHTML = 0;
        basknum.hidden = true;
    }

    // Cambio de precio de extras en sub
    document.querySelectorAll('input[type="checkbox"]').forEach((input) => {
        input.onchange = () => {
            const row = input.parentNode.parentNode.parentNode.id.replace('extras', '');
            const price = input.dataset.price;

            if (input.checked == true) {
                let sm = parseFloat(document.querySelector(`#subsmplace${row}`).value);
                let lg = parseFloat(document.querySelector(`#sublgplace${row}`).value);

                sm += parseFloat(price);
                lg += parseFloat(price);

                document.querySelector(`#subsmplace${row}`).value = sm.toFixed(2);
                document.querySelector(`#sublgplace${row}`).value = lg.toFixed(2);

                document.querySelector(`#subsmplace${row}`).innerHTML = `+ $${sm.toFixed(2)}`;
                document.querySelector(`#sublgplace${row}`).innerHTML = `+ $${lg.toFixed(2)}`;
            } else {
                let sm = parseFloat(document.querySelector(`#subsmplace${row}`).value);
                let lg = parseFloat(document.querySelector(`#sublgplace${row}`).value);

                sm -= parseFloat(price);
                lg -= parseFloat(price);

                document.querySelector(`#subsmplace${row}`).value = sm.toFixed(2);
                document.querySelector(`#sublgplace${row}`).value = lg.toFixed(2);

                document.querySelector(`#subsmplace${row}`).innerHTML = `+ $${sm.toFixed(2)}`;
                document.querySelector(`#sublgplace${row}`).innerHTML = `+ $${lg.toFixed(2)}`;
            }
        };
    });

    // Cambio de tamaño (pequeño/grande) en piz
    document.querySelectorAll('#pizlarge').forEach((input) => {
        input.onchange = () => {
            const row = input.dataset.row;

            document.querySelector(`#pizsmplace${row}`).hidden = true;
            document.querySelector(`#pizlgplace${row}`).hidden = false;
            input.className = 'btn btn-info active';
            input.checked = true;
            document.querySelector('#pizsmall').className = 'btn btn-info';
            document.querySelector('#pizsmall').checked = false;
        };
    });

    document.querySelectorAll('#pizsmall').forEach((input) => {
        input.onchange = () => {
            const row = input.dataset.row;

            document.querySelector(`#pizsmplace${row}`).hidden = false;
            document.querySelector(`#pizlgplace${row}`).hidden = true;
            input.className = 'btn btn-info active';
            input checked = true;
            document.querySelector('#pizlarge').className = 'btn btn-info';
            document.querySelector('#pizlarge').checked = false;
        };
    });

    // Cambio de tamaño (pequeño/grande) en sub
    document.querySelectorAll('#sublarge').forEach((input) => {
        input.onchange = () => {
            const row = input.dataset.row;

            document.querySelector(`#subsmplace${row}`).hidden = true;
            document.querySelector(`#sublgplace${row}`).hidden = false;
            input.className = 'btn btn-info active';
            input.checked = true;
            document.querySelector('#subsmall').className = 'btn btn-info';
            document.querySelector('#subsmall').checked = false;
        };
    });

    document.querySelectorAll('#subsmall').forEach((input) => {
        input.onchange = () => {
            const row = input.dataset.row;

            document.querySelector(`#subsmplace${row}`).hidden = false;
            document.querySelector(`#sublgplace${row}`).hidden = true;
            input.className = 'btn btn-info active';
            input.checked = true;
            document.querySelector('#sublarge').className = 'btn btn-info';
            document.querySelector('#sublarge').checked = false;
        };
    });

    // Cambio de tamaño (pequeño/grande) en platillos
    document.querySelectorAll('#platlarge').forEach((input) => {
        input.onchange = () => {
            const row = input.dataset.row;

            document.querySelector(`#platsmplace${row}`).hidden = true;
            document.querySelector(`#platlgplace${row}`).hidden = false;
            input.className = 'btn btn-info active';
            input.checked = true;
            document.querySelector('#platsmall').className = 'btn btn-info';
            document.querySelector('#platsmall').checked = false;
        };
    });

    document.querySelectorAll('#platsmall').forEach((input) => {
        input.onchange = () => {
            const row = input.dataset.row;

            document.querySelector(`#platsmplace${row}`).hidden = false;
            document.querySelector(`#platlgplace${row}`).hidden = true;
            input.className = 'btn btn-info active';
            input.checked = true;
            document.querySelector('#platlarge').className = 'btn btn-info';
            document.querySelector('#platlarge').checked = false;
        };
    });

    // Botones para realizar pedidos de tamaño pequeño
    document.querySelectorAll('.smplace').forEach((button) => {
        button.onclick = () => {
            const ident = button.dataset.ident;
            const size = 'small';
            const price = button.value;

            let tops = [];

            document.querySelectorAll(`#topSelect${ident}`).forEach((select) => {
                tops.push(select.selectedOptions[0].innerText);
            });

            const el = button.name;

            switch (el) {
                case 'pizsmplace':
                    data = {
                        'item': 'Pizza',
                        'ident': ident,
                        'type': button.dataset.typ,
                        'category': button.dataset.cat,
                        'size': size,
                        'toppings': tops,
                        'price': price
                    };

                    let pizquantity = document.querySelector(`#pizquant${ident}`);
                    pizquantity.innerHTML++;
                    pizquantity.hidden = false;

                    basknum.innerHTML++;
                    basknum.hidden = false;
                    break;
                case 'subsmplace':
                    document.querySelector(`#extras${ident}`).firstElementChild.firstElementChild.childNodes.forEach((input) => {
                        if (input.checked == true) {
                            tops.push(input.value);
                        }
                    });

                    data = {
                        'item': 'Sub',
                        'ident': ident,
                        'type': button.dataset.typ,
                        'size': size,
                        'toppings': tops,
                        'price': price
                    };

                    let subquantity = document.querySelector(`#subquant${ident}`);
                    subquantity.innerHTML++;
                    subquantity.hidden = false;

                    basknum.innerHTML++;
                    basknum.hidden = false;
                    break;
                case 'platsmplace':
                    data = {
                        'item': 'Platter',
                        'ident': ident,
                        'type': button.dataset.typ,
                        'size': size,
                        'price': price
                    };

                    let platquantity = document.querySelector(`#platterquant${ident}`);
                    platquantity.innerHTML++;
                    platquantity.hidden = false;

                    basknum.innerHTML++;
                    basknum.hidden = false;
                    break;
            }

            let bask = JSON.parse(localStorage.getItem('basket'));
            let subtotal = parseFloat(localStorage.getItem('subtotal'));
            let basketnum = JSON.parse(localStorage.getItem('basknum'));

            if (bask == null) {
                localStorage.setItem('basket', JSON.stringify([data]));
                localStorage.setItem('subtotal', data.price);
                localStorage.setItem('basknum', 1);
            } else {
                bask.push(data);
                localStorage.setItem('basket', JSON.stringify(bask));
                subtotal += parseFloat(data.price);
                localStorage.setItem('subtotal', subtotal);
                basketnum++;
                localStorage.setItem('basknum', basketnum);
            }

            button.blur();
        };
    });

    // Botones para realizar pedidos de tamaño grande
    document.querySelectorAll('.lgplace').forEach((button) => {
        button.onclick = () => {
            const ident = button.dataset.ident;
            const size = 'large';
            const price = button.value;
            let tops = [];

            document.querySelectorAll(`#topSelect${ident}`).forEach((select) => {
                tops.push(select.selectedOptions[0].innerHTML);
            });

            const el = button.name;

            switch (el) {
                case 'pizlgplace':
                    data = {
                        'item': 'Pizza',
                        'ident': ident,
                        'type': button.dataset.typ,
                        'category': button.dataset.cat,
                        'size': size,
                        'toppings': tops,
                        'price': price
                    };

                    let pizquantity = document.querySelector(`#pizquant${ident}`);
                    pizquantity.innerHTML++;
                    pizquantity.hidden = false;

                    basknum.innerHTML++;
                    basknum.hidden = false;
                    break;
                case 'sublgplace':
                    document.querySelector(`#extras${ident}`).firstElementChild.firstElementChild.childNodes.forEach((input) => {
                        if (input.checked == true) {
                            tops.push(input.value);
                        }
                    });

                    data = {
                        'item': 'Sub',
                        'ident': ident,
                        'type': button.dataset.typ,
                        'size': size,
                        'toppings': tops,
                        'price': price
                    };

                    let subquantity = document.querySelector(`#subquant${ident}`);
                    subquantity.innerHTML++;
                    subquantity.hidden = false;

                    basknum.innerHTML++;
                    basknum.hidden = false;
                    break;
                case 'platlgplace':
                    data = {
                        'item': 'Platter',
                        'ident': ident,
                        'type': button.dataset.typ,
                        'size': size,
                        'price': price
                    };

                    let platquantity = document.querySelector(`#platterquant${ident}`);
                    platquantity.innerHTML++;
                    platquantity.hidden = false;

                    basknum.innerHTML++;
                    basknum.hidden = false;
                    break;
            }

            let bask = JSON.parse(localStorage.getItem('basket'));
            let subtotal = parseFloat(localStorage.getItem('subtotal'));
            let basketnum = JSON.parse(localStorage.getItem('basknum'));

            if (bask == null) {
                localStorage.setItem('basket', JSON.stringify([data]));
                localStorage.setItem('subtotal', data.price);
                localStorage.setItem('basknum', 1);
            } else {
                bask.push(data);
                localStorage.setItem('basket', JSON.stringify(bask));
                subtotal += parseFloat(data.price);
                localStorage.setItem('subtotal', subtotal);
                basketnum++;
                localStorage.setItem('basknum', basketnum);
            }

            button.blur();
        };
    });

    // Botones para realizar pedidos sin indicar el tamaño
    document.querySelectorAll('.place').forEach((button) => {
        button.onclick = () => {
            const ident = button.dataset.ident;
            const price = button.value;
            let tops = [];
            const el = button.name;

            switch (el) {
                case 'pastaplace':
                    data = {
                        'item': 'Pasta',
                        'ident': ident,
                        'type': button.dataset.typ,
                        'price': price
                    };

                    let pastaquantity = document.querySelector(`#pastaquant${ident}`);
                    pastaquantity.innerHTML++;
                    pastaquantity.hidden = false;

                    basknum.innerHTML++;
                    basknum.hidden = false;
                    break;
                case 'saladplace':
                    data = {
                        'item': 'Salad',
                        'ident': ident,
                        'type': button.dataset.typ,
                        'price': price
                    };

                    let saladquantity = document.querySelector(`#saladquant${ident}`);
                    saladquantity.innerHTML++;
                    saladquantity hidden = false;

                    basknum.innerHTML++;
                    basknum.hidden = false;
                    break;
            }

            let bask = JSON.parse(localStorage.getItem('basket'));
            let subtotal = parseFloat(localStorage.getItem('subtotal'));
            let basketnum = JSON.parse(localStorage.getItem('basknum'));

            if (bask == null) {
                localStorage.setItem('basket', JSON.stringify([data]));
                localStorage.setItem('subtotal', data.price);
                localStorage.setItem('basknum', 1);
            } else {
                bask.push(data);
                localStorage.setItem('basket', JSON.stringify(bask));
                subtotal += parseFloat(data.price);
                localStorage.setItem('subtotal', subtotal);
                basketnum++;
                localStorage.setItem('basknum', basketnum);
            }

            button.blur();
        };
    });

    // Manejo de pestañas del menú
    document.querySelector('#pizzas').onclick = () => {
        document.querySelector('#pizzas').className = 'nav-link active';
        document.querySelector('#subs').className = 'nav-link';
        document.querySelector('#pasta').className = 'nav-link';
        document.querySelector('#salads').className = 'nav-link';
        document.querySelector('#platters').className = 'nav-link';

        document.querySelector('#pizzaBody').hidden = false;
        document.querySelector('#subBody').hidden = true;
        document.querySelector('#pastaBody').hidden = true;
        document.querySelector('#saladBody').hidden = true;
        document.querySelector('#platterBody').hidden = true;

        document.querySelector('#pizzas').blur();
    };

    document.querySelector('#subs').onclick = () => {
        document.querySelector('#pizzas').className = 'nav-link';
        document.querySelector('#subs').className = 'nav-link active';
        document.querySelector('#pasta').className = 'nav-link';
        document.querySelector('#salads').className = 'nav-link';
        document.querySelector('#platters').className = 'nav-link';

        document.querySelector('#pizzaBody').hidden = true;
        document.querySelector('#subBody').hidden = false;
        document.querySelector('#pastaBody').hidden = true;
        document.querySelector('#saladBody').hidden = true;
        document.querySelector('#platterBody').hidden = true;

        document.querySelector('#subs').blur();
    };

    document.querySelector('#pasta').onclick = () => {
        document.querySelector('#pizzas').className = 'nav-link';
        document.querySelector('#subs').className = 'nav-link';
        document.querySelector('#pasta').className = 'nav-link active';
        document.querySelector('#salads').className = 'nav-link';
        document.querySelector('#platters').className = 'nav-link';

        document.querySelector('#pizzaBody').hidden = true;
        document.querySelector('#subBody').hidden = true;
        document.querySelector('#pastaBody').hidden = false;
        document.querySelector('#saladBody').hidden = true;
        document.querySelector('#platterBody').hidden = true;

        document.querySelector('#pasta').blur();
    };

    document.querySelector('#salads').onclick = () => {
        document.querySelector('#pizzas').className = 'nav-link';
        document.querySelector('#subs').className = 'nav-link';
        document.querySelector('#pasta').className = 'nav-link';
        document.querySelector('#salads').className = 'nav-link active';
        document.querySelector('#platters').className = 'nav-link';

        document.querySelector('#pizzaBody').hidden = true;
        document.querySelector('#subBody').hidden = true;
        document.querySelector('#pastaBody').hidden = true;
        document.querySelector('#saladBody').hidden = false;
        document.querySelector('#platterBody').hidden = true;

        document.querySelector('#salads').blur();
    };

    document.querySelector('#platters').onclick = () => {
        document.querySelector('#pizzas').className = 'nav-link';
        document.querySelector('#subs').className = 'nav-link';
        document.querySelector('#pasta').className = 'nav-link';
        document.querySelector('#salads').className = 'nav-link';
        document.querySelector('#platters').className = 'nav-link active';

        document.querySelector('#pizzaBody').hidden = true;
        document.querySelector('#subBody').hidden = true;
        document.querySelector('#pastaBody').hidden = true;
        document.querySelector('#saladBody').hidden = true;
        document.querySelector('#platterBody').hidden = false;

        document.querySelector('#platters').blur();
    };
});
