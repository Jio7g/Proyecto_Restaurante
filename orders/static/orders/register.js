document.addEventListener('DOMContentLoaded', () => {
    
    // Evento que se ejecuta cuando se carga la página
    
    document.getElementById('username').onkeyup = () => {
        
        // Cuando se suelta una tecla en el campo de nombre de usuario

        const un = document.getElementById('username').value;

        if (un.length > 16 || un.length < 8) {

            // Si la longitud del nombre de usuario no cumple con los requisitos
            document.getElementById('unCheck').innerHTML = '<i class="far fa-times-circle"></i> El nombre de usuario no cumple con los requisitos.';
            document.getElementById('unCheck').hidden = false;
            document.getElementById('unCheck').className = 'alert alert-danger';
            document.getElementById('register').disabled = true;

        } else if (alphanum(un) == false) {

            // Si el nombre de usuario no es alfanumérico
            document.getElementById('unCheck').innerHTML = '<i class="far fa-times-circle"></i> El nombre de usuario no cumple con los requisitos.';
            document.getElementById('unCheck').hidden = false;
            document.getElementById('unCheck').className = 'alert alert-danger';
            document.getElementById('register').disabled = true;

        } else if (caseCheck(un) == false) {

            // Si el nombre de usuario no tiene al menos una letra mayúscula y una letra minúscula
            document.getElementById('unCheck').innerHTML = '<i class="far fa-times-circle"></i> El nombre de usuario no cumple con los requisitos.';
            document.getElementById('unCheck').hidden = false;
            document.getElementById('unCheck').className = 'alert alert-danger';
            document.getElementById('register').disabled = true;

        } else if (numCheck(un) == false) {

            // Si el nombre de usuario no contiene al menos un número
            document.getElementById('unCheck').innerHTML = '<i class="far fa-times-circle"></i> El nombre de usuario no cumple con los requisitos.';
            document.getElementById('unCheck').hidden = false;
            document.getElementById('unCheck').className = 'alert alert-danger';
            document.getElementById('register').disabled = true;

        } else {

            // Si el nombre de usuario cumple con todos los requisitos
            document.getElementById('unCheck').innerHTML = '<i class="far fa-check-circle"></i> El nombre de usuario cumple con los requisitos';
            document.getElementById('unCheck').hidden = false;
            document.getElementById('unCheck').className = 'alert alert-success';
            document.getElementById('register').disabled = false;
        }
    }

    document.getElementById('password').onkeyup = () => {

        // Cuando se suelta una tecla en el campo de contraseña

        const pw = document.getElementById('password').value;

        if (pw.length > 16 || pw.length < 8) {

            // Si la longitud de la contraseña no cumple con los requisitos
            document.getElementById('pwCheck').innerHTML = '<i class="far fa-times-circle"></i> La contraseña no cumple con los requisitos.';
            document.getElementById('pwCheck').hidden = false;
            document.getElementById('pwCheck').className = 'alert alert-danger';
            document.getElementById('register').disabled = true;

        } else if (alphanum(pw) == false) {

            // Si la contraseña no es alfanumérica
            document.getElementById('pwCheck').innerHTML = '<i class="far fa-times-circle"></i> La contraseña no cumple con los requisitos.';
            document.getElementById('pwCheck').hidden = false;
            document.getElementById('pwCheck').className = 'alert alert-danger';
            document.getElementById('register').disabled = true;

        } else if (caseCheck(pw) == false) {

            // Si la contraseña no tiene al menos una letra mayúscula y una letra minúscula
            document.getElementById('pwCheck').innerHTML = '<i class="far fa-times-circle"></i> La contraseña no cumple con los requisitos.';
            document.getElementById('pwCheck').hidden = false;
            document.getElementById('pwCheck').className = 'alert alert-danger';
            document.getElementById('register').disabled = true;

        } else if (numCheck(pw) == false) {

            // Si la contraseña no contiene al menos un número
            document.getElementById('pwCheck').innerHTML = '<i class="far fa-times-circle"></i> La contraseña no cumple con los requisitos.';
            document.getElementById('pwCheck').hidden = false;
            document.getElementById('pwCheck').className = 'alert alert-danger';
            document.getElementById('register').disabled = true;

        } else {

            // Si la contraseña cumple con todos los requisitos
            document.getElementById('pwCheck').innerHTML = '<i class="far fa-check-circle"></i> La contraseña cumple con los requisitos';
            document.getElementById('pwCheck').hidden = false;
            document.getElementById('pwCheck').className = 'alert alert-success';
            document.getElementById('register').disabled = false;
        }
    }

    document.getElementById('confirm').onkeyup = () => {

        // Cuando se suelta una tecla en el campo de confirmación de contraseña

        const pw = document.getElementById('password').value;
        const con = document.getElementById('confirm').value;

        if (pw != con) {

            // Si la contraseña y su confirmación no coinciden
            document.getElementById('pwMatch').innerHTML = '<i class="far fa-times-circle"></i> ¡Oops! Estas contraseñas no coinciden.';
            document.getElementById('pwMatch').hidden = false;
            document.getElementById('pwMatch').className = 'alert alert-danger';
            document.getElementById('register').disabled = true;

        } else {

            // Si la contraseña y su confirmación coinciden
            document.getElementById('pwMatch').innerHTML = '<i class="far fa-check-circle"></i> Las contraseñas coinciden.';
            document.getElementById('pwMatch').hidden = false;
            document.getElementById('pwMatch').className = 'alert alert-success';
            document.getElementById('register').disabled = false;
        }
    }
});

function alphanum(txt) {

    let allow = /^[0-9a-zA-Z]+$/;
    return allow.test(txt);
};

function caseCheck(txt) {
    
    let upcount = 0;
    let lowcount = 0;

    for (i = 0; i < txt.length; i++) {

        let c = txt[i];

        if (isNaN(c)) {

            if (c == c.toUpperCase()) {
                upcount++;
            }
            if (c == c.toLowerCase()) {
                lowcount++;
            }
        }
    }

    if (upcount >= 1 && lowcount >= 1) {
        return true;
    } else {
        return false;
    }
};

function numCheck(txt) {

    for (i = 0; i < txt.length; i++) {

        const c = txt[i];

        if (isNaN(c)) {
            continue;
        } else {
            return true;
        }
    }

    return false;
};