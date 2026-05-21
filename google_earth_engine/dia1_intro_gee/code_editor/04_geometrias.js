/**
 * Día 1 — Script 4: Geometrías, Features y operaciones espaciales
 * Curso de SIG y Teledetección · CHG
 *
 * Tres conceptos que NO son lo mismo:
 *   - Geometry          -> solo la forma (un punto, una línea, un polígono).
 *   - Feature           -> una geometría CON propiedades (nombre, población...).
 *   - FeatureCollection -> un conjunto de Features (≈ una capa vectorial).
 *
 * En este script las geometrías están definidas en el código para que
 * funcione tal cual. En clase también las dibujaremos con la herramienta
 * de geometrías del Code Editor (panel superior izquierdo del mapa).
 */

// --- Puntos de partida ---------------------------------------------------
var huelva  = ee.Geometry.Point([-6.9447, 37.2614]);
var sevilla = ee.Geometry.Point([-5.9845, 37.3891]);

// Polígono aproximado de la marisma de Doñana.
var Marisma = ee.Geometry.Polygon([[
  [-6.45, 37.10], [-6.18, 37.10], [-6.18, 36.85], [-6.45, 36.85]
]]);

// --- Buffers -------------------------------------------------------------
// buffer(distancia_en_metros) crea un área alrededor de una geometría.
var huelva_buffer  = huelva.buffer(50000);   // 50 km
var sevilla_buffer = sevilla.buffer(50000);

Map.addLayer(huelva_buffer,  {color: 'red'},  'Buffer Huelva');
Map.addLayer(sevilla_buffer, {color: 'blue'}, 'Buffer Sevilla');

// --- Operaciones espaciales ---------------------------------------------
// Intersección: el área COMÚN a las dos geometrías.
var intersection = huelva_buffer.intersection(sevilla_buffer);
Map.addLayer(intersection, {color: '00FF00'}, 'Intersección');

// Unión: combina las dos geometrías en una sola.
var union = huelva_buffer.union(sevilla_buffer);
Map.addLayer(union, {color: 'FF00FF'}, 'Unión');

// Diferencia: lo que está en la primera pero NO en la segunda.
var diff1 = huelva_buffer.difference(sevilla_buffer);
Map.addLayer(diff1, {color: 'FFFF00'}, 'Diferencia');

// Diferencia simétrica: lo que está en una o en otra, pero no en ambas.
var symDiff = huelva_buffer.symmetricDifference(sevilla_buffer);
Map.addLayer(symDiff, {color: '000000'}, 'Diferencia simétrica');

// Recortar la unión a la marisma (intersección con el polígono).
var clip_union = union.intersection(Marisma);
Map.addLayer(clip_union, {color: 'green'}, 'Unión recortada a la marisma');

// --- Propiedades de una geometría ---------------------------------------
print('Área de la marisma (m²):', Marisma.area());
print('Centroide de la marisma:', Marisma.centroid());
Map.addLayer(Marisma.centroid(), {color: 'white'}, 'Centroide marisma');

// --- Un Feature: geometría + propiedades --------------------------------
var puntoSevilla = ee.Feature(sevilla, {
  name: 'Sevilla',
  population: 688711
});
print('Feature de Sevilla:', puntoSevilla);
Map.addLayer(puntoSevilla, {color: 'green'}, 'Feature Sevilla');

// --- Una FeatureCollection: varios Features -----------------------------
var ciudades = ee.FeatureCollection([
  ee.Feature(ee.Geometry.Point([-5.9845, 37.3891]), {name: 'Sevilla',       population: 688711}),
  ee.Feature(ee.Geometry.Point([-6.9447, 37.2614]), {name: 'Huelva',        population: 144258}),
  ee.Feature(ee.Geometry.Point([-6.0839, 37.3404]), {name: 'Mairena',       population: 27493}),
  ee.Feature(ee.Geometry.Point([-6.3074, 37.2563]), {name: 'Villamanrique', population: 21076})
]);
print('FeatureCollection de ciudades:', ciudades);

// --- Estilizar Features dinámicamente -----------------------------------
// Una función que asigna un color según el nombre de cada ciudad.
var estilo = function (feature) {
  var nombre = ee.String(feature.get('name'));
  var color = ee.Algorithms.If(nombre.equals('Sevilla'), 'red',
              ee.Algorithms.If(nombre.equals('Huelva'),  'green',
              ee.Algorithms.If(nombre.equals('Mairena'), 'yellow', 'blue')));
  return feature.set({style: {color: color, pointSize: 10}});
};

var ciudadesEstilizadas = ciudades.map(estilo);
Map.addLayer(ciudadesEstilizadas.style({styleProperty: 'style'}), {}, 'Ciudades estilizadas');

// Centrar el mapa en la zona de trabajo.
Map.centerObject(ciudades, 9);

/**
 * EJERCICIO
 * 1. Dibuja un punto con la herramienta de geometrías y crea un buffer de 5 km.
 * 2. Añade tu municipio a la FeatureCollection 'ciudades' con su población.
 * 3. Calcula el área del buffer de Huelva con .area().
 */
