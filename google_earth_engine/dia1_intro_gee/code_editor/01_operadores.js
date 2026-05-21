/**
 * Día 1 — Script 1: Fundamentos de JavaScript (operadores)
 * Curso de SIG y Teledetección · CHG
 *
 * Cópialo en el Code Editor (https://code.earthengine.google.com)
 * y ejecútalo con el botón "Run". Mira la pestaña "Console" a la derecha.
 *
 * Antes de tocar imágenes de satélite necesitamos algo de JavaScript:
 * es el lenguaje del Code Editor de Earth Engine.
 */

// --- Imprimir en consola -------------------------------------------------
// print() escribe en la consola de Earth Engine (panel derecho).
// console.log() escribe en la consola del navegador (F12). Usaremos print().
print('Hello, GEE world!');
console.log('Hello, GEE world!');

// --- Variables -----------------------------------------------------------
// Declaramos variables con 'var'. El nombre describe lo que contiene.
var gee = 'Hello, GEE world!';
print(gee);

// Las comillas pueden ser simples o dobles:
print("'let's go'");

// --- Tipos de datos ------------------------------------------------------
var a = 10;            // número
var b = 3;             // número
var c = 5;             // número
var x = 5;             // número
var y = "5";           // string (texto), ¡no es lo mismo que el número 5!
var isAdult = true;    // booleano
var hasTicket = false; // booleano
var age = 18;          // número

// --- Operadores aritméticos ---------------------------------------------
print('Suma:', a + b);             // 13
print('Resta:', a - b);            // 7
print('Multiplicación:', a * b);   // 30
print('División:', a / b);         // 3.333...
print('Módulo (resto):', a % b);   // 1
print('Incremento (++a):', ++a);   // 11  -> a ahora vale 11
print('Decremento (--b):', --b);   // 2   -> b ahora vale 2

// --- Operadores de asignación -------------------------------------------
// 'c += 3' es una forma corta de escribir 'c = c + 3'.
c += 3;  print('+= :', c);  // 8
c -= 2;  print('-= :', c);  // 6
c *= 2;  print('*= :', c);  // 12
c /= 3;  print('/= :', c);  // 4
c %= 3;  print('%= :', c);  // 1

// --- Operadores de comparación ------------------------------------------
// OJO: == compara solo el valor; === compara valor Y tipo.
print('==  :', x == y);   // true  (5 == "5": el valor coincide)
print('=== :', x === y);  // false (número vs string: el tipo no coincide)
print('!=  :', x != y);   // false
print('!== :', x !== y);  // true
print('>   :', x > 3);    // true
print('<   :', x < 10);   // true
print('>=  :', x >= 5);   // true
print('<=  :', x <= 4);   // false

// --- Operadores lógicos --------------------------------------------------
print('AND (&&):', isAdult && hasTicket); // false (necesita los dos true)
print('OR  (||):', isAdult || hasTicket); // true  (basta con uno true)
print('NOT (!) :', !isAdult);             // false (invierte el booleano)

// --- Operador ternario ---------------------------------------------------
// condición ? valor_si_verdadero : valor_si_falso
var access = age >= 18 ? 'Acceso permitido' : 'Acceso denegado';
print('Acceso:', access);

/**
 * EJERCICIO
 * 1. Crea dos variables numéricas y calcula su producto.
 * 2. Crea una variable 'temperatura' y usa el operador ternario para
 *    imprimir 'Calor' si es > 30 o 'Templado' en caso contrario.
 */
