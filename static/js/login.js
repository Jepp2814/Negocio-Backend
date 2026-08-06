// ==============================
// RELOJ, FECHA Y SALUDO
// ==============================

const clock = document.getElementById("clock");
const date = document.getElementById("date");
const greeting = document.getElementById("greeting");

function actualizarReloj() {

    const ahora = new Date();

    // Hora
    clock.textContent = ahora.toLocaleTimeString("es-EC");

    // Fecha
    date.textContent = ahora.toLocaleDateString("es-EC", {
        weekday: "long",
        day: "numeric",
        month: "long",
        year: "numeric"
    });

    // Saludo
    const hora = ahora.getHours();

    if (hora < 12) {
        greeting.textContent = "Buenos días";
    } else if (hora < 18) {
        greeting.textContent = "Buenas tardes";
    } else {
        greeting.textContent = "Buenas noches";
    }
}

actualizarReloj();
setInterval(actualizarReloj, 1000);

const form = document.querySelector("form");

if(form){

    form.addEventListener("submit",function(){

        const boton=document.getElementById("loginButton");
        const contenido=document.getElementById("buttonContent");

        boton.disabled=true;

        contenido.innerHTML=`
        <i class="fa-solid fa-gear fa-spin"></i>
        Verificando...
        `;

    });

}
const passwordInput=document.getElementById("current-password");

const togglePassword=document.getElementById("togglePassword");

if(togglePassword){

    function mostrar(){

        passwordInput.type="text";

    }

    function ocultar(){

        passwordInput.type="password";

    }

    togglePassword.addEventListener("mousedown",mostrar);

    togglePassword.addEventListener("mouseup",ocultar);

    togglePassword.addEventListener("mouseleave",ocultar);

    togglePassword.addEventListener("touchstart",mostrar);

    togglePassword.addEventListener("touchend",ocultar);

}
function actualizarHora(){

    const ahora=new Date();

    const opcionesHora={
        hour:"numeric",
        minute:"2-digit",
        hour12: true
        
    };

    const opcionesFecha={
        weekday:"long",
        day:"numeric",
        month:"long",
        year:"numeric"
    };

    document.getElementById("clock").innerHTML=
        ahora.toLocaleTimeString("es-EC",opcionesHora);

    document.getElementById("date").innerHTML=
        ahora.toLocaleDateString("es-EC",opcionesFecha);

    const hora=ahora.getHours();

    let saludo="";

    if(hora<12)
        saludo="Buenos días";
    else if(hora<18)
        saludo="Buenas tardes";
    else
        saludo="Buenas noches";

    document.getElementById("greeting").innerHTML=saludo;

}

setInterval(actualizarHora,1000);

actualizarHora();
