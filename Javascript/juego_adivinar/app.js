let numeroSecreto = 0;
let intentos = 0;
let listaNumerosSorteados = [];
let numeroMaximo = 10;

function asignarTextoElemento(elemento, texto) {
    let elementoHTML = document.querySelector(elemento);
    elementoHTML.innerHTML = texto;
    return;
}

function verificarIntento() {
    // Preguntar número
    let numeroDeUsuario = parseInt(document.getElementById('valorUsuario').value);
    // Verificar si el número es correcto
    if (numeroDeUsuario === numeroSecreto) {
        asignarTextoElemento('p', `¡Acertaste! Lo hiciste en ${intentos} ${intentos == 1 ? 'intento': 'intentos'}`);
        document.getElementById('reiniciar').removeAttribute('disabled');
    } else {
        // El usuario no acertó
        if (numeroDeUsuario > numeroSecreto){
            asignarTextoElemento('p', 'El número secreto es menor!'); 
        } else {
            asignarTextoElemento('p', 'El número secreto es mayor!');
        }
        intentos++;
        limpiarCaja();
    }
    return;
}

function limpiarCaja() {
    document.getElementById('valorUsuario').value = '';
}

function generarNumeroSecreto() {
    let numeroGenerado = Math.floor(Math.random()*numeroMaximo+1);
    //console.log(numeroGenerado);
    console.log(listaNumerosSorteados);
    //Si ya sorteamos todos los números
    if (listaNumerosSorteados.length == numeroMaximo) {
        asignarTextoElemento('p', 'Se sorteraon todos los números posibles!\nReinicio automático.');
        listaNumerosSorteados = [];
        return generarNumeroSecreto();
    } else {
        //Si el número generado está en la lista

        if (listaNumerosSorteados.includes(numeroGenerado)) {
            return generarNumeroSecreto();
        } else {
            listaNumerosSorteados.push(numeroGenerado);
            return numeroGenerado;
        }
    }
}

function condicionesIniciales() {
    asignarTextoElemento('h1', 'Juego del número secreto');
    asignarTextoElemento('p', `Ingresa un número entre 1 y ${numeroMaximo}!`);
    numeroSecreto = generarNumeroSecreto();
    intentos = 1;
    console.log(`Número generado: ${numeroSecreto}`);
}

function reiniciarJuego(){
    //Limpiar caja
    limpiarCaja();
    //Mensaje inicio
    //Generar número
    //Iniciar intentos
    condicionesIniciales();
    //Deshabiliar botón
    document.querySelector('#reiniciar').setAttribute('disabled','true');
}

condicionesIniciales();


///////////////////////
/* DESAFÍO OPCIONAL-1*/
///////////////////////

/* Desafío 1: Cambia el contenido de la etiqueta h1 con document.querySelector
document.querySelector('h1').textContent = "Hora del Desafío";

// Desafío 2: Crea una función que muestre en la consola el mensaje "El botón fue clicado" siempre que se presione el botón "Console"
document.querySelector('#console-btn').addEventListener('click', function() {
  console.log("El botón fue clicado");
});

// Desafío 3: Crea una función que se ejecute cuando se haga clic en el botón "prompt", preguntando el nombre de una ciudad de Brasil
document.querySelector('#prompt-btn').addEventListener('click', function() {
  var ciudad = prompt("¿Cuál es el nombre de una ciudad de Brasil?");
  alert("Estuve en " + ciudad + " y me acordé de ti");
});

// Desafío 4: Crea una función que muestre una alerta con el mensaje: "Yo amo JS" siempre que se presione el botón "Alerta"
document.querySelector('#alert-btn').addEventListener('click', function() {
  alert("Yo amo JS");
});

// Desafío 5: Al hacer clic en el botón "suma", pide 2 números y muestra el resultado de la suma en una alerta
document.querySelector('#suma-btn').addEventListener('click', function() {
  var num1 = parseInt(prompt("Ingrese el primer número"));
  var num2 = parseInt(prompt("Ingrese el segundo número"));
  var resultado = num1 + num2;
  alert("El resultado de la suma es: " + resultado);
}); */

///////////////////////
/* DESAFÍO OPCIONAL-2*/
///////////////////////

// Función que muestra "¡Hola, mundo!" en la consola
/* function saludar() {
    console.log("¡Hola, mundo!");
  }
  
  // Función que recibe un nombre como parámetro y muestra "¡Hola, [nombre]!" en la consola
  function saludarNombre(nombre) {
    console.log(`¡Hola, ${nombre}!`);
  }
  
  // Función que recibe un número como parámetro y devuelve el doble de ese número
  function doble(numero) {
    return numero * 2;
  }
  
  // Función que recibe tres números como parámetros y devuelve su promedio
  function promedio(a, b, c) {
    return (a + b + c) / 3;
  }
  
  // Función que recibe dos números como parámetros y devuelve el mayor de ellos
  function mayor(a, b) {
    return a > b ? a : b;
  }
  
  // Función que recibe un número como parámetro y devuelve el resultado de multiplicar ese número por sí mismo
  function cuadrado(numero) {
    return numero * numero;
  }
  
  // Ejemplos de uso:
  saludar(); // Muestra "¡Hola, mundo!" en la consola
  saludarNombre("Juan"); // Muestra "¡Hola, Juan!" en la consola
  console.log(doble(5)); // Muestra 10 en la consola
  console.log(promedio(2, 4, 6)); // Muestra 4 en la consola
  console.log(mayor(3, 5)); // Muestra 5 en la consola
  console.log(cuadrado(4)); // Muestra 16 en la consola */

///////////////////////
/* DESAFÍO OPCIONAL-3*/
///////////////////////

/* // Función para calcular el índice de masa corporal (IMC)
function calcularIMC(altura, peso) {
    // Fórmula para calcular el IMC: peso / altura^2
    const imc = parseInt(peso / (altura ** 2));
    let explicaImc = '';
    if (imc <= 18.5) {
        explicaImc = 'Bajo peso'
    } else if (imc >18.5 && imc <= 24.9) {
        explicaImc = 'Peso normal'
    } else if (imc >24.9 && imc <=29.9) {
        explicaImc = 'Sobrepeso'
    } else {
        explicaImc = 'Obesidad'
    }
    return `Altura: ${altura} m. Peso: ${peso} kg.\nEl IMC es: ${imc}.\nResultado: ${explicaImc}.`;
  }
  
  // Función para calcular el factorial de un número
  function calcularFactorial(numero) {
    // Inicializamos el factorial en 1
    let factorial = 1;
    // Iteramos desde 1 hasta el número pasado como parámetro
    for (let i = 1; i <= numero; i++) {
      // Multiplicamos el factorial por el número actual
      factorial *= i;
    }
    return factorial;
  }
  
  // Función para convertir dólares a reales
  function convertirDolaresAReales(dolares) {
    // Cotización del dólar en reales: R$4,80
    const cotizacion = 4.80;
    // Convertimos los dólares a reales
    const reales = dolares * cotizacion;
    return reales;
  }
  
  // Función para calcular el área y perímetro de una sala rectangular
  function calcularAreaYPerimetroRectangular(altura, anchura) {
    // Calculamos el área: altura * anchura
    const area = altura * anchura;
    // Calculamos el perímetro: 2 * (altura + anchura)
    const perimetro = 2 * (altura + anchura);
    console.log(`Área: ${area} m²`);
    console.log(`Perímetro: ${perimetro} m`);
  }
  
  // Función para calcular el área y perímetro de una sala circular
  function calcularAreaYPerimetroCircular(radio) {
    // Calculamos el área: π * radio^2
    const area = 3.14 * (radio ** 2);
    // Calculamos el perímetro: 2 * π * radio
    const perimetro = 2 * 3.14 * radio;
    console.log(`Área: ${area} m²`);
    console.log(`Perímetro: ${perimetro} m`);
  }
  
  // Función para mostrar la tabla de multiplicar de un número
  function mostrarTablaDeMultiplicar(numero) {
    console.log(`Tabla de multiplicar del ${numero}:`);
    for (let i = 0; i <= 10; i++) {
      console.log(`${numero} x ${i} = ${numero * i}`);
    }
  }
  
  // Ejemplos de uso:
  console.log(calcularIMC(1.73, 68)); // IMC de una persona de 1.75m y 65kg
  console.log(calcularFactorial(5)); // Factorial de 5
  console.log(convertirDolaresAReales(10)); // Convertir 10 dólares a reales
  calcularAreaYPerimetroRectangular(5, 3); // Área y perímetro de una sala rectangular de 5m x 3m
  calcularAreaYPerimetroCircular(4); // Área y perímetro de una sala circular de radio 4m
  mostrarTablaDeMultiplicar(7); // Tabla de multiplicar del 7 */

///////////////////////
/* DESAFÍO OPCIONAL-4*/
///////////////////////

/* // 1. Crea una lista vacía llamada "listaGenerica"
let listaGenerica = [];

// 2. Crea una lista de lenguajes de programación llamada "lenguagesDeProgramacion"
let lenguagesDeProgramacion = ['JavaScript', 'C', 'C++', 'Kotlin', 'Python'];

// 3. Agrega a la lista "lenguagesDeProgramacion" los siguientes elementos: 'Java', 'Ruby' y 'GoLang'
lenguagesDeProgramacion.push('Java', 'Ruby', 'GoLang');

// 4. Crea una función que muestre en la consola todos los elementos de la lista "lenguagesDeProgramacion"
function mostrarLenguajes() {
  console.log('Lenguajes de programación:');
  for (let i = 0; i < lenguagesDeProgramacion.length; i++) {
    console.log(`  ${lenguagesDeProgramacion[i]}`);
  }
}

// 5. Crea una función que muestre en la consola todos los elementos de la lista "lenguagesDeProgramacion" en orden inverso
function mostrarLenguajesInverso() {
  console.log('Lenguajes de programación en orden inverso:');
  for (let i = lenguagesDeProgramacion.length - 1; i >= 0; i--) {
    console.log(`  ${lenguagesDeProgramacion[i]}`);
  }
}

// 6. Crea una función que calcule el promedio de los elementos en una lista de números
function calcularPromedio(listaNumeros) {
  let suma = 0;
  for (let i = 0; i < listaNumeros.length; i++) {
    suma += listaNumeros[i];
  }
  return suma / listaNumeros.length;
}

// 7. Crea una función que muestre en la consola el número más grande y el número más pequeño en una lista
function mostrarMinMax(listaNumeros) {
  let max = listaNumeros[0];
  let min = listaNumeros[0];
  for (let i = 1; i < listaNumeros.length; i++) {
    if (listaNumeros[i] > max) {
      max = listaNumeros[i];
    }
    if (listaNumeros[i] < min) {
      min = listaNumeros[i];
    }
  }
  console.log(`Mínimo: ${min}, Máximo: ${max}`);
}

// 8. Crea una función que devuelva la suma de todos los elementos en una lista
function sumarLista(listaNumeros) {
  let suma = 0;
  for (let i = 0; i < listaNumeros.length; i++) {
    suma += listaNumeros[i];
  }
  return suma;
}

// 9. Crea una función que devuelva la posición en la lista donde se encuentra un elemento pasado como parámetro, o -1 si no existe en la lista
function buscarElemento(lista, elemento) {
  for (let i = 0; i < lista.length; i++) {
    if (lista[i] === elemento) {
      return i;
    }
  }
  return -1;
}

// 10. Crea una función que reciba dos listas de números del mismo tamaño y devuelva una nueva lista con la suma de los elementos uno a uno
function sumarListas(lista1, lista2) {
  let resultado = [];
  for (let i = 0; i < lista1.length; i++) {
    resultado.push(lista1[i] + lista2[i]);
  }
  return resultado;
}

// 11. Crea una función que reciba una lista de números y devuelva una nueva lista con el cuadrado de cada número
function cuadradosLista(listaNumeros) {
  let resultado = [];
  for (let i = 0; i < listaNumeros.length; i++) {
    resultado.push(listaNumeros[i] * listaNumeros[i]);
  }
  return resultado;
} */

