"""
Generador del notebook del Día 1 de Google Earth Engine.
Construye gee_geemap_intro.ipynb de forma idempotente.
Ejecutar con: python _build_notebook.py

Basado en el material del repositorio GEE_Course_2024 (día 5),
reescrito en español y reorganizado para el curso de la CHG.
"""
import json
import uuid
import pathlib

HERE = pathlib.Path(__file__).parent


def cell(kind, src):
    if isinstance(src, str):
        src = src.splitlines(keepends=True)
    cid = uuid.uuid4().hex[:12]
    base = {"cell_type": kind, "id": cid, "metadata": {}, "source": src}
    if kind == "code":
        base["execution_count"] = None
        base["outputs"] = []
    return base


def md(src):
    return cell("markdown", src)


def code(src):
    return cell("code", src)


cells = []

# =====================================================================
# Portada
# =====================================================================
cells.append(md("""\
# Introducción a Google Earth Engine con Python (`geemap`)

**Curso de SIG y Teledetección · Confederación Hidrográfica del Guadalquivir**

Día 1 — Google Earth Engine

---

En el Code Editor hemos trabajado GEE con **JavaScript**. Este notebook hace
lo mismo desde **Python**, usando la librería [`geemap`](https://geemap.org/),
que conecta Earth Engine con mapas interactivos en el navegador.

La API es casi idéntica: lo que en JavaScript era `Map.addLayer(...)`, en
Python es `Map.addLayer(...)`; lo que era `ee.Image(...)` sigue siendo
`ee.Image(...)`. Cambia la sintaxis del lenguaje, no los conceptos.

**Recuerda el concepto clave:** sigue habiendo un mundo *cliente* (este
notebook) y un mundo *servidor* (los objetos `ee.*`, que se calculan en
Google). `getInfo()` trae un valor del servidor al cliente.

Ejecuta las celdas en orden con `Shift + Enter`.
"""))

# =====================================================================
# 1. Instalación y autenticación
# =====================================================================
cells.append(md("""\
## 1. Instalación y autenticación

`geemap` no viene preinstalado en Colab: lo instalamos con `pip`. La
instalación dura solo mientras la sesión esté activa.
"""))

cells.append(code("# Instalar geemap (solo necesario en Colab)\n!pip install -q geemap"))

cells.append(code("""\
import ee
import geemap"""))

cells.append(md("""\
La primera vez tendrás que **autenticarte**: `ee.Authenticate()` abre una
ventana para iniciar sesión con tu cuenta de Google y autorizar Earth Engine.

En `ee.Initialize()` hay que indicar el **ID de tu proyecto** de Google Cloud
(el que registraste en Earth Engine). Sustituye `'tu-proyecto-gee'` por el tuyo.
"""))

cells.append(code("""\
ee.Authenticate()
ee.Initialize(project='tu-proyecto-gee')  # <-- cambia esto por tu project ID"""))

# =====================================================================
# 2. Mapa interactivo
# =====================================================================
cells.append(md("""\
## 2. El mapa interactivo

`geemap.Map()` crea un mapa interactivo. Sobre él iremos añadiendo capas con
`Map.addLayer()`. Ejecuta la celda y aparecerá el mapa debajo.
"""))

cells.append(code("""\
Map = geemap.Map()
Map"""))

cells.append(md("""\
Puedes elegir el mapa base de fondo. `'HYBRID'` muestra la ortofoto con
etiquetas de Google, muy útil para reconocer el terreno.
"""))

cells.append(code("""\
Map = geemap.Map(center=[37.0, -6.0], zoom=8, basemap='HYBRID')
Map"""))

# =====================================================================
# 3. ee.Image
# =====================================================================
cells.append(md("""\
## 3. Trabajar con imágenes: `ee.Image`

Un **`ee.Image`** es un raster: una o varias bandas, cada una con su nombre,
su tipo de dato y su resolución.

Empezamos con un modelo digital de elevación global, el **SRTM**, que es una
imagen de una sola banda (`elevation`).
"""))

cells.append(code("""\
Map = geemap.Map(center=[37.0, -4.5], zoom=7)

# Cargar el modelo digital de elevación SRTM
dem = ee.Image('CGIAR/SRTM90_V4')
Map.addLayer(dem, {}, 'DEM (sin estilo)')
Map"""))

cells.append(md("""\
Sin parámetros de visualización (`{}`) la imagen se ve plana. Hay que indicar
a Earth Engine **cómo** pintarla: valores mínimo y máximo, y una paleta de
colores.
"""))

cells.append(code("""\
vis_dem = {
    'min': 0,
    'max': 2000,
    'palette': ['006633', 'E5FFCC', '662A00', 'D8D8D8', 'F5F5F5'],
}
Map.addLayer(dem, vis_dem, 'DEM (con paleta)')
Map"""))

cells.append(md("""\
### Una imagen Landsat

Cargamos ahora una escena **Landsat 8** sobre Doñana. Es la colección 2,
nivel 2 (reflectividad de superficie). Tiene varias bandas: `SR_B1` a `SR_B7`,
además de bandas de calidad.

`Map.centerObject()` centra el mapa automáticamente sobre la imagen.
"""))

cells.append(code("""\
Map = geemap.Map()

# Escena Landsat 8 sobre Doñana (path/row 202/034)
image = ee.Image('LANDSAT/LC08/C02/T1_L2/LC08_202034_20240722')

Map.centerObject(image, zoom=9)
Map.addLayer(image, {}, 'Landsat (sin estilo)')
Map"""))

# =====================================================================
# 4. Visualización
# =====================================================================
cells.append(md("""\
## 4. Visualización: composiciones de color

Una imagen Landsat tiene muchas bandas. Para verla elegimos **tres bandas**
que se asignan a los canales rojo, verde y azul de la pantalla.

- **Color natural:** `SR_B4` (rojo), `SR_B3` (verde), `SR_B2` (azul).
- **Falso color infrarrojo:** `SR_B5` (NIR), `SR_B4`, `SR_B3`. La vegetación
  aparece en rojo intenso porque refleja mucho en el infrarrojo cercano.
"""))

cells.append(code("""\
Map = geemap.Map()
Map.centerObject(image, zoom=9)

# Composición en color natural
vis_natural = {'bands': ['SR_B4', 'SR_B3', 'SR_B2'], 'min': 7000, 'max': 18000}
Map.addLayer(image, vis_natural, 'Color natural')

# Composición en falso color infrarrojo
vis_falso = {'bands': ['SR_B5', 'SR_B4', 'SR_B3'], 'min': 8000, 'max': 25000}
Map.addLayer(image, vis_falso, 'Falso color (vegetación en rojo)')

Map"""))

cells.append(md("""\
### El factor de escala

Las bandas de Landsat Colección 2 no guardan la reflectividad directamente,
sino un número entero. Para obtener la **reflectividad real** (valores de 0 a 1)
hay que aplicar un factor de escala y un desplazamiento:

`reflectividad = valor * 0.0000275 - 0.2`

Trabajar con reflectividad real es importante para calcular índices.
"""))

cells.append(code("""\
# Aplicar el factor de escala a las bandas de reflectividad
image_sr = image.multiply(0.0000275).add(-0.2)

Map = geemap.Map()
Map.centerObject(image, zoom=9)
vis_refl = {'bands': ['SR_B4', 'SR_B3', 'SR_B2'], 'min': 0, 'max': 0.3}
Map.addLayer(image_sr, vis_refl, 'Reflectividad (color natural)')
Map"""))

# =====================================================================
# 5. Metadatos
# =====================================================================
cells.append(md("""\
## 5. Metadatos de una imagen

Cada imagen lleva información asociada: nombres de banda, resolución,
fecha, cobertura de nubes... Para verla desde Python imprimimos el
resultado de `getInfo()`, que trae el valor del servidor al cliente.
"""))

cells.append(code("""\
# Nombres de las bandas
band_names = image.bandNames()
print('Bandas:', band_names.getInfo())"""))

cells.append(code("""\
# Resolución (tamaño de píxel, en metros) de la banda SR_B1
escala = image.select('SR_B1').projection().nominalScale()
print('Resolución (m):', escala.getInfo())"""))

cells.append(code("""\
# Cobertura de nubes de la escena
nubes = image.get('CLOUD_COVER')
print('Cobertura de nubes (%):', nubes.getInfo())"""))

cells.append(code("""\
# Fecha de adquisición
fecha = ee.Date(image.get('system:time_start'))
print('Fecha:', fecha.format('YYYY-MM-dd').getInfo())"""))

cells.append(code("""\
# Resumen completo de propiedades con geemap
geemap.image_props(image).getInfo()"""))

# =====================================================================
# 6. Operaciones matemáticas: índices
# =====================================================================
cells.append(md("""\
## 6. Operaciones matemáticas: índices espectrales

Earth Engine aplica las operaciones **píxel a píxel**. Esto nos permite
combinar bandas para calcular índices.

### NDVI — índice de vegetación

El NDVI mide el vigor de la vegetación a partir del infrarrojo cercano (NIR)
y el rojo (RED):

`NDVI = (NIR - RED) / (NIR + RED)`

Hay dos formas de calcularlo. **A mano**, con operaciones de banda:
"""))

cells.append(code("""\
nir = image_sr.select('SR_B5')
red = image_sr.select('SR_B4')

ndvi_manual = nir.subtract(red).divide(nir.add(red))"""))

cells.append(md("""\
O con el método **`normalizedDifference()`**, que hace exactamente esa
fórmula `(a - b) / (a + b)`. Es la forma recomendada:
"""))

cells.append(code("""\
ndvi = image_sr.normalizedDifference(['SR_B5', 'SR_B4']).rename('NDVI')

Map = geemap.Map()
Map.centerObject(image, zoom=9)
vis_ndvi = {
    'min': 0,
    'max': 0.8,
    'palette': ['a8d5e2', 'f9a620', 'ffd449', '548c2f', '104911'],
}
Map.addLayer(ndvi, vis_ndvi, 'NDVI')
Map"""))

cells.append(md("""\
### NDWI — índice de agua

El mismo método sirve para el agua, combinando el verde y el infrarrojo
cercano. El agua tiene valores altos de NDWI.
"""))

cells.append(code("""\
ndwi = image_sr.normalizedDifference(['SR_B3', 'SR_B5']).rename('NDWI')

Map = geemap.Map()
Map.centerObject(image, zoom=9)
vis_ndwi = {'min': 0, 'max': 1, 'palette': ['ffffff', '0000ff']}
Map.addLayer(ndwi, vis_ndwi, 'NDWI')
Map"""))

cells.append(md("""\
### Expresiones

Para fórmulas más complejas conviene `expression()`: se escribe la fórmula
como texto y se indica qué banda es cada variable. Aquí el **EVI**, una
mejora del NDVI que corrige efectos del suelo y la atmósfera:
"""))

cells.append(code("""\
evi = image_sr.expression(
    '2.5 * ((NIR - RED) / (NIR + 6 * RED - 7.5 * BLUE + 1))',
    {
        'NIR': image_sr.select('SR_B5'),
        'RED': image_sr.select('SR_B4'),
        'BLUE': image_sr.select('SR_B2'),
    },
).rename('EVI')

Map = geemap.Map()
Map.centerObject(image, zoom=9)
Map.addLayer(evi, vis_ndvi, 'EVI')
Map"""))

# =====================================================================
# 7. Operaciones condicionales: máscaras
# =====================================================================
cells.append(md("""\
## 7. Operaciones condicionales: máscaras

Los operadores relacionales (`gt`, `lt`, `gte`...) comparan píxel a píxel y
devuelven 1 (verdadero) o 0 (falso).

Por ejemplo, los píxeles con NDWI mayor que 0 son, aproximadamente, agua:
"""))

cells.append(code("""\
agua = ndwi.gt(0)

Map = geemap.Map()
Map.centerObject(image, zoom=9)
Map.addLayer(agua, {'min': 0, 'max': 1, 'palette': ['white', 'blue']}, 'Agua (0/1)')
Map"""))

cells.append(md("""\
Con `updateMask()` ocultamos los píxeles que no nos interesan. Si
enmascaramos el agua consigo misma, los píxeles de tierra (valor 0)
desaparecen y solo queda el agua visible:
"""))

cells.append(code("""\
agua_mask = agua.updateMask(agua)

Map = geemap.Map(basemap='HYBRID')
Map.centerObject(image, zoom=9)
Map.addLayer(agua_mask, {'palette': ['00BFFF']}, 'Solo agua')
Map"""))

# =====================================================================
# 8. ImageCollection
# =====================================================================
cells.append(md("""\
## 8. Colecciones de imágenes: `ee.ImageCollection`

Una **`ImageCollection`** es un conjunto de imágenes: por ejemplo, *todas*
las escenas Landsat 8 disponibles. Como son cientos de miles, lo primero
es **filtrar** para quedarnos con las que nos interesan.
"""))

cells.append(code("""\
coleccion = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
print('Imágenes en toda la colección:', coleccion.size().getInfo())"""))

cells.append(md("""\
Tres filtros básicos, que se pueden encadenar:

- **`filterDate()`** — por rango de fechas.
- **`filterBounds()`** — por una zona geográfica.
- **`filter()`** con `ee.Filter` — por metadatos (p. ej. cobertura de nubes).
"""))

cells.append(code("""\
# Punto de referencia: Doñana
roi = ee.Geometry.Point([-6.40, 37.00])

filtrada = (ee.ImageCollection('LANDSAT/LC08/C02/T1_L2')
            .filterDate('2024-01-01', '2024-12-31')
            .filterBounds(roi)
            .filter(ee.Filter.lt('CLOUD_COVER', 20))
            .sort('CLOUD_COVER'))

print('Imágenes tras filtrar:', filtrada.size().getInfo())"""))

cells.append(md("""\
`.first()` toma la primera imagen de la colección. Como hemos ordenado por
`CLOUD_COVER`, será la **menos nubosa** del año:
"""))

cells.append(code("""\
mejor = filtrada.first()
print('Nubes de la mejor imagen (%):', mejor.get('CLOUD_COVER').getInfo())

Map = geemap.Map()
Map.centerObject(mejor, zoom=8)
vis = {'bands': ['SR_B5', 'SR_B4', 'SR_B3'], 'min': 8000, 'max': 25000}
Map.addLayer(mejor, vis, 'Imagen menos nubosa de 2024')
Map"""))

cells.append(md("""\
### Reducir una colección a una imagen

Con `median()` (u otros reductores: `mean()`, `max()`...) se combinan todas
las imágenes de la colección en **una sola**, tomando para cada píxel la
mediana de todas las fechas. Es una forma sencilla de obtener una imagen
sin nubes.
"""))

cells.append(code("""\
compuesta = filtrada.median()

Map = geemap.Map()
Map.centerObject(roi, zoom=9)
Map.addLayer(compuesta, vis, 'Compuesta anual (mediana)')
Map"""))

cells.append(md("""\
### Consultar valores de la colección

`aggregate_array()` recoge el valor de una propiedad en todas las imágenes:
"""))

cells.append(code("""\
# Cobertura de nubes de cada imagen filtrada
filtrada.aggregate_array('CLOUD_COVER').getInfo()"""))

# =====================================================================
# 9. Datos vectoriales
# =====================================================================
cells.append(md("""\
## 9. Datos vectoriales: `FeatureCollection`

Earth Engine también trabaja con datos vectoriales. Además del catálogo
público, puedes **subir tus propios vectoriales** como *assets* y, si los
compartes, cualquiera puede cargarlos por su identificador.

Aquí usamos un asset de municipios de Andalucía
(`users/digdgeografo/curso_GEE/Andalucia`) compartido públicamente: lo
cargamos igual que un dataset del catálogo, indicando su ruta.
"""))

cells.append(code("""\
andalucia = ee.FeatureCollection('users/digdgeografo/curso_GEE/Andalucia')

Map = geemap.Map()
Map.centerObject(andalucia, zoom=7)
Map.addLayer(andalucia, {'color': 'gray'}, 'Municipios de Andalucía')
Map"""))

cells.append(md("""\
Una `FeatureCollection` se **filtra** con `ee.Filter`, igual que una
colección de imágenes. Cada Feature tiene propiedades (aquí, `nombre` y
`provincia`). Nos quedamos con el municipio de **Almonte**, en Doñana:
"""))

cells.append(code("""\
almonte = andalucia.filter(ee.Filter.eq('nombre', 'Almonte'))

Map = geemap.Map()
Map.centerObject(almonte, zoom=10)
Map.addLayer(almonte, {'color': 'red'}, 'Almonte')
Map"""))

cells.append(md("""\
`clip()` recorta una imagen a la geometría de una FeatureCollection. Así
recortamos el NDVI al término municipal de Almonte:
"""))

cells.append(code("""\
ndvi_almonte = ndvi.clip(almonte)

Map = geemap.Map()
Map.centerObject(almonte, zoom=10)
Map.addLayer(ndvi_almonte, vis_ndvi, 'NDVI recortado a Almonte')
Map"""))

# =====================================================================
# 10. Cierre y ejercicios
# =====================================================================
cells.append(md("""\
## 10. Resumen del día

Hoy hemos visto que:

- GEE tiene un mundo **cliente** y un mundo **servidor**; `getInfo()` los conecta.
- Una **`ee.Image`** es un raster; se visualiza con parámetros (`min`, `max`,
  `bands`, `palette`).
- Las operaciones se aplican **píxel a píxel**: así se calculan índices como
  el NDVI o el NDWI.
- Una **`ImageCollection`** se **filtra** (fecha, lugar, metadatos) y se puede
  **reducir** a una sola imagen.
- Las **`FeatureCollection`** son datos vectoriales; con `clip()` recortamos
  rasters a una zona.

### Ejercicios para practicar

1. Carga la escena Landsat y muéstrala en falso color con otros valores de
   `min` y `max`. ¿Cómo cambia la imagen?
2. Calcula el índice **MNDWI** (`(SR_B3 - SR_B6) / (SR_B3 + SR_B6)`) y
   compáralo con el NDWI.
3. Filtra la colección Landsat para el **verano de 2023** sobre Doñana y
   quédate con la imagen menos nubosa.
4. Filtra el asset de Andalucía por `provincia` (p. ej. `'Huelva'`) y
   recorta el NDVI a esa provincia.
5. Cambia la paleta del NDVI por una tuya y ajusta el rango de visualización.
"""))

# =====================================================================
nb = {
    "cells": cells,
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python"},
        "colab": {"provenance": []},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

out = HERE / "gee_geemap_intro.ipynb"
out.write_text(json.dumps(nb, indent=1, ensure_ascii=False))
print(f"Escrito {out}  ({out.stat().st_size / 1024:.1f} KB, {len(cells)} celdas)")
