# Introducción a Google Earth Engine

## ¿Qué es Google Earth Engine?

**Google Earth Engine (GEE)** es una plataforma en la nube para el análisis geoespacial a escala planetaria. Combina tres cosas:

- Un **catálogo de datos** público y enorme: décadas de imágenes de satélite (Landsat, Sentinel, MODIS...), modelos digitales de elevación, climatología, coberturas del suelo y mucho más, ya preprocesado y listo para usar.
- La **potencia de cálculo** de la infraestructura de Google: los análisis se ejecutan en miles de servidores en paralelo, no en tu ordenador.
- Una **API** (interfaz de programación) para describir los análisis, disponible en **JavaScript** y en **Python**.

La idea clave: en vez de descargar gigabytes de imágenes a tu ordenador, **envías el análisis a los datos**. Tú escribes una "receta" y Google la ejecuta donde están las imágenes.

Es gratuito para uso académico, educativo y de investigación.

---

## ¿Por qué usar GEE?

- No hay que descargar ni almacenar imágenes: el catálogo ya está en la nube.
- No hace falta un ordenador potente: el cálculo ocurre en los servidores de Google.
- Permite trabajar con series temporales largas y zonas extensas sin esfuerzo.
- Los datos llegan ya corregidos y organizados en colecciones homogéneas.
- Resultados reproducibles: un script es la descripción completa de un análisis.

**Limitaciones a tener en cuenta:** depende de tener conexión y cuenta activa, los cálculos muy pesados pueden agotar la memoria, y la exportación de resultados grandes lleva su tiempo.

---

## Las tres formas de trabajar con GEE

| Herramienta | Lenguaje | Para qué sirve |
|-------------|----------|----------------|
| **Earth Engine Explorer** | — (interfaz visual) | Explorar el catálogo y visualizar datos sin programar |
| **Code Editor** | JavaScript | Entorno principal para desarrollar y probar análisis |
| **API de Python (`geemap`)** | Python | Integrar GEE en flujos de trabajo de Python y notebooks |

En este curso usaremos las tres. **Hoy** empezamos por el **Code Editor** y terminamos viendo un **notebook de Python** con `geemap` en Google Colab.

---

## Configuración previa: cuenta y proyecto

Desde 2025, para usar Earth Engine es obligatorio tener un **proyecto de Google Cloud** vinculado. Los pasos, resumidos:

1. **Cuenta de Google.** Sirve tu cuenta de Gmail habitual.
2. **Crear un proyecto de Google Cloud** en [console.cloud.google.com](https://console.cloud.google.com) (por ejemplo `curso-gee-chg`).
3. **Registrar el proyecto en Earth Engine** en [code.earthengine.google.com/register](https://code.earthengine.google.com/register), eligiendo el uso **no comercial** (gratuito, para investigación y educación).
4. **Habilitar la Earth Engine API** para ese proyecto.

> **Error más habitual:** crear el proyecto con una cuenta de Google y entrar al Code Editor con otra distinta. Usa **siempre la misma cuenta** en todo el proceso.

Una vez configurado, accede al Code Editor en **[code.earthengine.google.com](https://code.earthengine.google.com)**.

---

## El Code Editor

El Code Editor es un entorno de desarrollo web. Sus paneles principales:

- **Panel central (Map):** el mapa interactivo donde se muestran los resultados. Arriba a la izquierda están las herramientas de **geometría** para dibujar puntos, líneas y polígonos.
- **Editor de código (centro):** donde escribes el script en JavaScript. El botón **Run** lo ejecuta.
- **Panel izquierdo:**
  - *Scripts*: tus scripts guardados y los ejemplos.
  - *Docs*: la documentación de toda la API, buscable.
  - *Assets*: tus datos subidos (shapes, rasters propios).
- **Panel derecho:**
  - *Console*: la salida de `print()` y los mensajes de error.
  - *Inspector*: pincha en el mapa para consultar el valor de los píxeles.
  - *Tasks*: las exportaciones a Google Drive o Assets.

---

## El concepto más importante: cliente vs servidor

Es la idea que más cuesta al principio y la que conviene tener clara desde el día 1.

Cuando escribes código en GEE conviven **dos mundos**:

- **Cliente:** tu navegador. Ejecuta JavaScript "normal": variables, bucles `for`, condicionales `if`.
- **Servidor:** los ordenadores de Google. Ejecutan los objetos que empiezan por `ee.` (`ee.Image`, `ee.Number`, `ee.FeatureCollection`...).

Cuando escribes `ee.Image(...)` **no se calcula nada todavía**: solo construyes una *descripción* del análisis. El cálculo real ocurre en el servidor cuando pides un resultado (al imprimirlo, al mostrarlo en el mapa o al exportarlo).

**Consecuencias prácticas:**

- No uses bucles `for` sobre objetos `ee.*`. Usa **`.map()`**, que aplica una función a cada elemento de una colección en paralelo.
- No uses `if/else` sobre valores `ee.*`. Usa **`ee.Algorithms.If()`**.
- `getInfo()` trae un valor del servidor al cliente, pero **detiene el código** mientras espera. Úsalo de forma puntual, nunca dentro de un bucle ni con datos grandes.

```javascript
// Mundo cliente: un string normal de JavaScript
var saludo = 'Hola';

// Mundo servidor: un objeto que vive en Google
var saludoEE = ee.String('Hola');
```

---

## El catálogo de datos

Earth Engine organiza los datos en tres tipos de objetos:

- **`Image`** — un raster: una o varias bandas (una imagen Landsat, un modelo de elevación...).
- **`ImageCollection`** — un conjunto de imágenes (toda la serie Landsat 8, por ejemplo). Se filtra por fecha, lugar y metadatos.
- **`Feature` / `FeatureCollection`** — datos vectoriales: geometrías con propiedades (municipios, estaciones de aforo...).

Puedes explorar todo lo disponible en el [catálogo oficial](https://developers.google.com/earth-engine/datasets), con la descripción de cada conjunto, sus bandas y el identificador para cargarlo.

---

## Casos de uso típicos

GEE se usa habitualmente para:

- Cálculo de índices espectrales (NDVI, NDWI...) y su evolución temporal.
- Detección de cambios: deforestación, urbanización, láminas de agua.
- Seguimiento de inundaciones y sequías.
- Clasificación de coberturas del suelo.
- Estadísticas zonales sobre municipios, cuencas o parcelas.

En el contexto de la **Confederación Hidrográfica del Guadalquivir**, encaja especialmente bien en el seguimiento de embalses y láminas de agua, el estado de la vegetación de ribera y el análisis multitemporal de la cuenca.

---

## Plan del día 1

1. **Earth Engine Explorer** — un primer vistazo visual al catálogo, sin código.
2. **Code Editor** — fundamentos de JavaScript y primeros objetos de GEE, con los scripts de la carpeta [`code_editor/`](./code_editor/):
   - `01_operadores.js` — variables y operadores.
   - `02_diccionarios.js` — diccionarios (objetos).
   - `03_client_server.js` — cliente vs servidor.
   - `04_geometrias.js` — geometrías, Features y operaciones espaciales.
   - `05_puntos_tamano.js` — símbolos proporcionales.
3. **Notebook en Colab** — la misma idea desde Python con `geemap`: ver el notebook [`gee_geemap_intro.ipynb`](./gee_geemap_intro.ipynb).

---

## Recursos

**Documentación oficial**

- [Guía de inicio de Earth Engine](https://developers.google.com/earth-engine/guides/getstarted)
- [Cliente vs servidor](https://developers.google.com/earth-engine/guides/client_server)
- [Catálogo de datos](https://developers.google.com/earth-engine/datasets)
- [Documentación de geemap](https://geemap.org/)

**Herramientas**

- [Earth Engine Code Editor](https://code.earthengine.google.com)
- [Earth Engine Explorer](https://explorer.earthengine.google.com)
- [Google Colab](https://colab.research.google.com)

**Comunidad**

- [GEE Developers Forum](https://groups.google.com/g/google-earth-engine-developers)
- [GEE en GIS Stack Exchange](https://gis.stackexchange.com/questions/tagged/google-earth-engine)
