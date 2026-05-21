/**
 * Día 1 — Script 3: Cliente vs Servidor  ⚠️ EL CONCEPTO MÁS IMPORTANTE
 * Curso de SIG y Teledetección · CHG
 *
 * Earth Engine tiene DOS mundos:
 *   - CLIENTE: tu navegador. Ejecuta JavaScript "normal" (var, for, if...).
 *   - SERVIDOR: los ordenadores de Google. Ejecutan los objetos ee.*
 *
 * El código que escribes en el navegador solo construye una "receta".
 * El cálculo de verdad ocurre en el servidor cuando pides un resultado.
 */

// --- Objeto cliente vs objeto servidor ----------------------------------
var clientString = 'I am a String';
print('Tipo (cliente):', typeof clientString);   // string

var serverString = ee.String('I am not a String!');
print('Tipo (servidor):', typeof serverString);  // object
print('¿Es un objeto EE?', serverString instanceof ee.ComputedObject); // true

// Al imprimir un objeto del servidor, Earth Engine lo evalúa por ti.
print('Contenido del ee.String:', serverString);

// --- getInfo(): traer un valor del servidor al cliente ------------------
// getInfo() DETIENE el código y espera la respuesta del servidor.
// Úsalo con cuidado: nunca dentro de bucles ni con datos grandes.
var someString = serverString.getInfo();      // ahora es un string de cliente
var strings = someString + '  Am I?';
print('Concatenado en el cliente:', strings);

// --- Bucles: lado cliente -----------------------------------------------
// Un for tradicional funciona... pero solo con datos de cliente.
var clientList = [];
for (var i = 1; i <= 10; i++) {
  clientList.push(i % 2 === 0 ? i + 10 : i);
}
print('Lista construida con un for (cliente):', clientList);

// --- Bucles: lado servidor con .map() -----------------------------------
// Con objetos ee.* NO usamos for. Usamos .map(): aplica una función
// a cada elemento de la colección, en paralelo, en el servidor.
var serverList = ee.List.sequence(0, 10);
serverList = serverList.map(function (n) {
  return ee.Number(n).add(1);
});
print('Lista construida con .map() (servidor):', serverList);

// --- Condicionales en el servidor: ee.Algorithms.If ---------------------
// El if/else de JavaScript NO entiende objetos del servidor.
// Para decidir sobre un valor del servidor usamos ee.Algorithms.If().
var updatedList = ee.List.sequence(1, 10).map(function (n) {
  var number = ee.Number(n);
  return ee.Algorithms.If(number.mod(2).eq(0), number.add(100), number);
});
print('Pares +100 con ee.Algorithms.If:', updatedList);

// --- El error clásico: mezclar mundos -----------------------------------
var myList = ee.List([1, 2, 3]);
var serverBoolean = myList.contains(5);  // objeto servidor (ee.Boolean)

// ❌ MAL: un if de cliente sobre un booleano de servidor.
// El objeto ee.* "existe", así que el if SIEMPRE lo trata como verdadero.
var clientConditional;
if (serverBoolean) {
  clientConditional = true;
} else {
  clientConditional = false;
}
print('if de cliente (resultado ERRÓNEO):', clientConditional); // true (¡mal!)

// ✅ BIEN: dejamos la decisión en el servidor.
var serverConditional = ee.Algorithms.If(serverBoolean, 'Sí', 'No');
print('ee.Algorithms.If (resultado correcto):', serverConditional); // No

/**
 * RESUMEN
 *  - Objetos ee.*  -> servidor.   Variables normales -> cliente.
 *  - No uses for ni if/else con objetos ee.*  -> usa .map() y ee.Algorithms.If.
 *  - getInfo() solo de forma puntual, nunca dentro de bucles.
 */
