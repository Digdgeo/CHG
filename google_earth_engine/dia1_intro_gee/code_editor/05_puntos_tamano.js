/**
 * Día 1 — Script 5: Símbolos proporcionales (puntos de tamaño variable)
 * Curso de SIG y Teledetección · CHG
 *
 * Objetivo: dibujar ciudades como puntos cuyo tamaño depende de su
 * población. Es un mapa de "símbolos proporcionales".
 */

// --- Colección de puntos con propiedades --------------------------------
var puntos = ee.FeatureCollection([
  ee.Feature(ee.Geometry.Point([-6.0074, 37.3824]), {nombre: 'Sevilla', poblacion: 100000}),
  ee.Feature(ee.Geometry.Point([-6.9447, 37.2614]), {nombre: 'Huelva',  poblacion: 200000}),
  ee.Feature(ee.Geometry.Point([-5.9272, 37.3891]), {nombre: 'Otro',    poblacion: 50000})
]);

// --- Función de estilo ---------------------------------------------------
// Calcula el tamaño del punto a partir de la población.
// El divisor y el tamaño base se ajustan a ojo según los datos.
var asignarEstilo = function (feature) {
  var poblacion = ee.Number(feature.get('poblacion'));
  var pointSize = poblacion.divide(20000).add(5);
  return feature.set({style: {color: 'blue', pointSize: pointSize}});
};

// --- Aplicar el estilo a cada punto -------------------------------------
var puntosEstilizados = puntos.map(asignarEstilo);

// --- Mostrar en el mapa --------------------------------------------------
Map.addLayer(puntosEstilizados.style({styleProperty: 'style'}), {}, 'Símbolos proporcionales');
Map.centerObject(puntos, 9);

/**
 * EJERCICIO
 * 1. Añade dos ciudades más con sus poblaciones reales.
 * 2. Cambia el color de los puntos a rojo.
 * 3. Prueba a usar la raíz cuadrada de la población (.sqrt()) para el
 *    tamaño: compara el resultado con la escala lineal anterior.
 */
