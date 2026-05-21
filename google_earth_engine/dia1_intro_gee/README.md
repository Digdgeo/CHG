# Día 1 — Introducción a Google Earth Engine

Primera sesión del módulo de **Google Earth Engine (GEE)**. Hoy nos familiarizamos con la plataforma: empezamos con el **Code Editor** y JavaScript, y terminamos viendo un **notebook de Python** con `geemap` en Google Colab.

## Objetivos

- Entender qué es GEE y cómo se organiza (catálogo, Code Editor, API de Python).
- Manejar los fundamentos de JavaScript necesarios para el Code Editor.
- Asimilar el concepto **cliente vs servidor**, el más importante de GEE.
- Trabajar con geometrías, `Image` e `ImageCollection`.

## Material

| Archivo | Contenido |
|---------|-----------|
| [`introduccion_gee.md`](./introduccion_gee.md) · [`introduccion_gee.pdf`](./introduccion_gee.pdf) | **Guía de referencia**: qué es GEE, configuración de la cuenta, el Code Editor, el concepto cliente/servidor, el catálogo de datos y casos de uso. |
| [`code_editor/`](./code_editor/) | Scripts de JavaScript para ejecutar en el [Code Editor](https://code.earthengine.google.com). |
| [`gee_geemap_intro.ipynb`](./gee_geemap_intro.ipynb) | Notebook de Python con `geemap`: `Image`, visualización, metadatos, índices, máscaras, `ImageCollection` y datos vectoriales. |
| [`_build_notebook.py`](./_build_notebook.py) | Script que genera el notebook de forma idempotente. |

## Parte 1 — Code Editor (JavaScript)

Copia cada script en el [Code Editor](https://code.earthengine.google.com) y ejecútalo con **Run**. Antes, conviene un primer vistazo visual al catálogo con el [Earth Engine Explorer](https://explorer.earthengine.google.com).

| Nº | Script | Contenido |
|----|--------|-----------|
| 01 | [`01_operadores.js`](./code_editor/01_operadores.js) | Variables, tipos de datos y operadores (aritméticos, comparación, lógicos, ternario). |
| 02 | [`02_diccionarios.js`](./code_editor/02_diccionarios.js) | Diccionarios (objetos): crear, acceder, modificar, anidar. `ee.Dictionary`. |
| 03 | [`03_client_server.js`](./code_editor/03_client_server.js) | **Cliente vs servidor**: objetos `ee.*`, `.map()` frente a bucles `for`, `ee.Algorithms.If`, `getInfo()`. |
| 04 | [`04_geometrias.js`](./code_editor/04_geometrias.js) | Geometrías, buffers, operaciones espaciales (intersección, unión, diferencia), `Feature` y `FeatureCollection`. |
| 05 | [`05_puntos_tamano.js`](./code_editor/05_puntos_tamano.js) | Símbolos proporcionales: estilizar puntos según una propiedad numérica. |

## Parte 2 — Notebook en Google Colab (Python)

El notebook `gee_geemap_intro.ipynb` repite los conceptos desde Python con la librería [`geemap`](https://geemap.org/). Cubre el mapa interactivo, `ee.Image`, visualización, metadatos, índices espectrales (NDVI, NDWI, EVI), máscaras, `ee.ImageCollection` (filtros y reductores) y `FeatureCollection`.

Trabaja con una escena **Landsat 8 sobre Doñana** (`LC08_202034_20240722`), datasets del catálogo y un **asset público de municipios de Andalucía** (`users/digdgeografo/curso_GEE/Andalucia`) — no necesita ningún fichero local. La sección de vectoriales sirve además para explicar cómo subir y compartir *assets* propios.

### Abrir directamente en Colab

Cambia `github.com` por `githubtocolab.com` en la URL del notebook:

```
https://githubtocolab.com/Digdgeo/CHG/blob/main/google_earth_engine/dia1_intro_gee/gee_geemap_intro.ipynb
```

> **Requisito previo:** una cuenta de Google Earth Engine con un proyecto de Google Cloud registrado. En la celda `ee.Initialize(project='tu-proyecto-gee')` hay que poner el **ID de tu proyecto**. Los pasos de configuración están en `introduccion_gee.md`.
