alert(`¡Bienvenidos al juego del número secreto, en este juego
deberás adivinar el número que yo te he puesto!`);

// Variables
let numeroMaximoPosible = 10
let numeroSecreto = Math.floor(Math.random()*numeroMaximoPosible)+1;
let numeroUsuario = 0;
let intentos = 1;
let intentosMaximos = 3;
while (numeroUsuario != numeroSecreto) {
    numeroUsuario = parseInt(prompt(`¿Me indicas un número entre 1 y ${numeroMaximoPosible} por favor?`));
    
    // Almacena el número de usuario en consola
    console.log(`Valor: ${numeroUsuario}. Tipo: ${typeof(numeroUsuario)}`);

    // Este código realiza la comprobación
    if (numeroUsuario == numeroSecreto) {
        // Acertamos, fue verdadera la condición
        //alert(`¡Acertaste! El número secreto es: ${numeroSecreto}.\nLo hiciste en ${intentos} ${palabraVeces}.`);
        alert(`¡Acertaste! El número secreto es: ${numeroSecreto}.\nLo hiciste en ${intentos} ${intentos == 1 ? 'intento' : 'intentos'}.`);
    } else {
        // No acertamos, fue falsa la condición
        if (numeroUsuario > numeroSecreto) {
            alert('El número secreto es menor');
        } else {
            alert('El número secreto es mayor');
        }
        // Incrementa el contador
        intentos++;
        //palabraVeces = 'intentos';
        if (intentos > intentosMaximos){
            alert(`¡Perdiste! Llegaste al número máximo de ${intentosMaximos} intentos.\nEl número secreto es ${numeroSecreto}.`);
            break;
        }
        //alert(`¡Lo siento! El número secreto es ${numeroSecreto}`);
        //alert(`¡Lo siento! No acertaste el número`);
    }
}

//#####################
/* DESAFÍO OPCIONAL-1*/
//#####################
/* 
// Muestra una alerta con el mensaje "¡Bienvenida y bienvenido a nuestro sitio web!"
alert("¡Bienvenida y bienvenido a nuestro sitio web!");

// Declara una variable llamada nombre y asígnale el valor "Luna"
let nombre = "Luna";

// Crea una variable llamada edad y asígnale el valor 25
let edad = 25;

// Establece una variable numeroDeVentas y asígnale el valor 50
let numeroDeVentas = 50;

// Establece una variable saldoDisponible y asígnale el valor 1000
let saldoDisponible = 1000;

// Muestra una alerta con el texto "¡Error! Completa todos los campos"
// alert("¡Error! Completa todos los campos");

// Declara una variable llamada mensajeDeError y asígnale el valor "¡Error! Completa todos los campos"
let mensajeDeError = "¡Error! Completa todos los campos";

// Muestra una alerta con el valor de la variable mensajeDeError
alert(mensajeDeError);

// Utiliza un prompt para preguntar el nombre del usuario y almacénalo en la variable nombre
nombre = prompt("¿Cuál es tu nombre?");
console.log(nombre);

// Pide al usuario que ingrese su edad usando un prompt y almacénala en la variable edad
edad = parseInt(prompt("¿Cuál es tu edad?"));

// Ahora, si la edad es mayor o igual a 18, muestra una alerta con el mensaje "¡Puedes obtener tu licencia de conducir!"
if (edad >= 18) {
  alert("¡Puedes obtener tu licencia de conducir!");
} */

//#####################
/* DESAFÍO OPCIONAL-2*/
//#####################
/* // Desafío 1: Día de la semana
const dia = prompt("¿Qué día de la semana es?");
if (dia === "Sábado" || dia === "Domingo") {
  alert("¡Buen fin de semana!");
} else {
  alert("¡Buena semana!");
}

// Desafío 2: Número positivo o negativo
const numero = parseInt(prompt("Ingresa un número"));
if (numero > 0) {
  alert("El número es positivo");
} else if (numero < 0) {
  alert("El número es negativo");
} else {
  alert("El número es cero");
}

// Desafío 3: Sistema de puntuación
const puntuacion = parseInt(prompt("Ingresa tu puntuación"));
if (puntuacion >= 100) {
  alert("¡Felicidades, has ganado!");
} else {
  alert("Intentalo nuevamente para ganar.");
}

// Desafío 4: Saldo de la cuenta
const saldo = 1000; // valor del saldo
const mensaje = `Tu saldo actual es de ${saldo} pesos.`;
alert(mensaje);

// Desafío 5: Bienvenida con nombre
const nombre = prompt("Ingresa tu nombre");
const mensajeBienvenida = `Bienvenido, ${nombre}!`;
alert(mensajeBienvenida); */

//#####################
/* DESAFÍO OPCIONAL-3*/
//#####################
/* // Desafío 1: Contador de 1 a 10
let i = 1;
while (i <= 10) {
  console.log(`Contador: ${i}`);
  i++;
  }
  console.log("Fin del ciclo");

// Desafío 2: Contador de 10 a 0
let j = 10;
while (j >= 0) {
  console.log(`Contador: ${j}`);
  j--;
  }
  console.log("Fin del ciclo");

// Desafío 3: Programa de cuenta progresiva
let num = parseInt(prompt("Ingrese un número: "));
let k = 0;nombre
while (k <= num) {
  console.log(`Contador: ${k}`);
  k++;
  }
  console.log("Fin del ciclo"); */

//#####################
/* DESAFÍO OPCIONAL-4*/
//#####################
/* 
// Desafío 1: Mostrar un mensaje de bienvenida
console.log("¡Bienvenido!");

// Desafío 2: Mostrar un mensaje personalizado con el nombre
var nombre = "Juan";
console.log(`¡Hola, ${nombre}!`);

// Desafío 3: Mostrar un mensaje personalizado con el nombre utilizando alert
var nombre = "Juan";
alert(`¡Hola, ${nombre}!`);

// Desafío 4: Preguntar al usuario su lenguaje de programación favorito
var lenguaje = prompt("¿Cuál es el lenguaje de programación que más te gusta?");
console.log(`Tu lenguaje de programación favorito es ${lenguaje}`);

// Desafío 5: Realizar la suma de dos números
var valor1 = 5;
var valor2 = 3;
var resultado = valor1 + valor2;
console.log(`La suma de ${valor1} y ${valor2} es igual a ${resultado}`);

// Desafío 6: Realizar la resta de dos números
var valor1 = 5;
var valor2 = 3;
var resultado = valor1 - valor2;
console.log(`La diferencia entre ${valor1} y ${valor2} es igual a ${resultado}`);

// Desafío 7: Verificar si una persona es mayor o menor de edad
var edad = parseInt(prompt("¿Cuál es tu edad?"));
if (edad >= 18) {
  console.log("Eres mayor de edad");
} else {
  console.log("Eres menor de edad");
}

// Desafío 8: Verificar si un número es positivo, negativo o cero
var numero = parseInt(prompt("Ingresa un número"));
if (numero > 0) {
  console.log("El número es positivo");
} else if (numero < 0) {
  console.log("El número es negativo");
} else {
  console.log("El número es cero");
}

// Desafío 9: Mostrar los números del 1 al 10 utilizando un bucle while
var i = 1;
while (i <= 10) {
  console.log(i);
  i++;
}

// Desafío 10: Verificar si una nota es aprobatoria o no
var nota = 8;
if (nota >= 7) {
  console.log("Aprobado");
} else {
  console.log("Reprobado");
}

// Desafío 11: Generar un número aleatorio
var numeroAleatorio = Math.random();
console.log(`El número aleatorio es ${numeroAleatorio}`);

// Desafío 12: Generar un número entero aleatorio entre 1 y 10
var numeroAleatorio = Math.floor(Math.random() * 10) + 1;
console.log(`El número aleatorio es ${numeroAleatorio}`);

// Desafío 13: Generar un número entero aleatorio entre 1 y 1000
var numeroAleatorio = Math.floor(Math.random() * 1000) + 1;
console.log(`El número aleatorio es ${numeroAleatorio}`); */