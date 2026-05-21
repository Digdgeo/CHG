/**
 * Día 1 — Script 2: Diccionarios (objetos de JavaScript)
 * Curso de SIG y Teledetección · CHG
 *
 * Un diccionario (u "objeto") guarda datos como pares clave: valor.
 * Es la estructura que más usaremos para parámetros de visualización,
 * propiedades de Features, etc.
 */

// --- Crear un diccionario ------------------------------------------------
// Las claves van a la izquierda de los dos puntos; los valores a la derecha.
var persona = {
  nombre: 'Juan',
  edad: 30,
  ciudad: 'Madrid',
  profesion: 'Ingeniero'
};

print('Diccionario completo:', persona);

// --- Acceder a los valores ----------------------------------------------
// Hay dos notaciones equivalentes: con punto o con corchetes.
print('Notación de punto:', persona.nombre);     // Juan
print('Notación de corchetes:', persona['edad']); // 30

// --- Añadir una propiedad nueva -----------------------------------------
persona.pais = 'España';
print('Tras añadir país:', persona.pais);

// --- Modificar una propiedad existente ----------------------------------
persona.edad = 31;
print('Tras modificar edad:', persona.edad);

// --- Eliminar una propiedad ---------------------------------------------
delete persona.ciudad;
print('Tras eliminar ciudad:', persona);

// --- Diccionarios anidados ----------------------------------------------
// Un valor puede ser, a su vez, otro diccionario.
var ciudad = {
  nombre: 'Sevilla',
  poblacion: 688711,
  coordenadas: { lon: -5.9845, lat: 37.3891 }
};
print('Coordenada lon:', ciudad.coordenadas.lon);

/**
 * NOTA — diccionario de JavaScript vs ee.Dictionary
 * El objeto { } de arriba vive en el navegador (lado cliente).
 * Earth Engine también tiene su propio ee.Dictionary, que vive en
 * los servidores de Google (lado servidor). Lo veremos en el script 3.
 */
var eeDict = ee.Dictionary({ banda: 'NIR', escala: 30 });
print('ee.Dictionary (objeto del servidor):', eeDict);
print('Valor de "escala":', eeDict.get('escala'));

/**
 * EJERCICIO
 * Crea un diccionario con la información de tu municipio:
 * nombre, población y un diccionario anidado con sus coordenadas.
 */
