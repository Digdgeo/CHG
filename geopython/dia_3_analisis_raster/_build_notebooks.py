"""
Generador de los notebooks del Día 3 (análisis raster).
Construye 03a_intro_numpy.ipynb y 03b_rasterio_indices_mascaras.ipynb
de forma idempotente. Ejecutar con: python _build_notebooks.py
"""
import json, uuid, pathlib

HERE = pathlib.Path(__file__).parent


def cell(kind, src):
    if isinstance(src, str):
        src = src.splitlines(keepends=True)
        # garantiza que cada línea menos la última termine en \n, y la última no
        src = [s if s.endswith("\n") else s for s in src]
    cid = uuid.uuid4().hex[:12]
    base = {"cell_type": kind, "id": cid, "metadata": {}, "source": src}
    if kind == "code":
        base["execution_count"] = None
        base["outputs"] = []
    return base


def write_nb(filename, cells):
    nb = {
        "cells": cells,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python"},
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    out = HERE / filename
    out.write_text(json.dumps(nb, indent=1, ensure_ascii=False))
    print(f"Wrote {out}  ({out.stat().st_size/1024:.1f} KB, {len(cells)} cells)")


# =====================================================================
# 03a — NumPy aplicado a rasters
# =====================================================================
A = []

A.append(cell("markdown", """\
# CHG — Análisis Raster con Python
## Día 3 · Módulo A: NumPy — el lenguaje de los rasters

**Curso de Python para el Análisis Espacial**
Confederación Hidrográfica del Guadalquivir

---

> **Idea fuerza del día:** un raster (una imagen Landsat, un MDT, una máscara de agua…) es internamente **un array de NumPy**. Aprender NumPy es aprender a hacer teledetección.

## Contenidos

1. ¿Por qué NumPy en SIG/teledetección?
2. Creación de arrays
3. Atributos (ndim, shape, dtype) → leídos como propiedades de un raster
4. Indexación y *slicing* — recortar ventanas
5. Álgebra elemento a elemento — la base del NDVI
6. Reshape, stack y concatenación — apilar bandas
7. Funciones universales (`np.log`, `np.sqrt`, `np.where`…)
8. Estadística por eje (`axis`)
9. **Máscaras booleanas** — la base de NDWI binarizado, *no data*, clasificación
10. Mini-ejercicios contextualizados (NDVI, máscara de agua, clorofila)
"""))

A.append(cell("markdown", """\
## 1. ¿Por qué NumPy en SIG/teledetección?

Una imagen Landsat tiene, por ejemplo, **7711 × 7581 píxeles** y **6 bandas**. Son **~350 millones de números**. Si los recorremos con un `for` de Python, tardamos minutos. Con NumPy, segundos.

NumPy ofrece:
- **Arrays N-dimensionales** (`ndarray`): 2D = una banda; 3D = (bandas, alto, ancho).
- **Operaciones vectorizadas** — `(nir - red) / (nir + red)` se aplica píxel a píxel sin bucles.
- **Máscaras booleanas** — `agua = ndwi > 0.3` te devuelve un raster binario en una línea.

Casi todo el ecosistema geoespacial (rasterio, xarray, rioxarray, scikit-image, GDAL, GEE en Python…) trabaja **internamente con `ndarray`**.
"""))

A.append(cell("code", "import numpy as np\nprint(f'NumPy {np.__version__}')"))

A.append(cell("markdown", """\
---
## 2. Creación de arrays

### 2.1 Desde listas (uso ocasional, típicamente con pocos valores)
"""))

A.append(cell("code", """\
# Vector de valores NDVI medidos en 5 píxeles
ndvi_pixeles = np.array([0.12, 0.55, 0.78, 0.04, -0.10])
print(ndvi_pixeles)
print('Tipo:', ndvi_pixeles.dtype)
"""))

A.append(cell("code", """\
# Un mini-raster 3x3 (escribiéndolo a mano)
mini_raster = np.array([
    [0.10, 0.12, 0.08],   # fila 0
    [0.45, 0.52, 0.50],   # fila 1
    [0.78, 0.82, 0.80],   # fila 2
])
print(mini_raster)
print('shape:', mini_raster.shape)   # (filas, columnas)
"""))

A.append(cell("markdown", """\
### 2.2 Arrays inicializados (lo más habitual)

| Función              | Para qué sirve en raster                              |
|----------------------|--------------------------------------------------------|
| `np.zeros(shape)`    | Crear una máscara o un raster vacío                    |
| `np.ones(shape)`     | Inicializar pesos, multiplicadores                     |
| `np.full(shape, v)`  | Rellenar con valor `nodata`                            |
| `np.arange(n)`       | Series temporales, índices                             |
| `np.linspace(a,b,n)` | Generar bordes para clasificar                         |
| `np.random.rand(*s)` | Datos sintéticos para probar algoritmos                |
"""))

A.append(cell("code", """\
# Máscara vacía con la misma forma que el mini-raster
mascara = np.zeros(mini_raster.shape, dtype='uint8')
print(mascara)
print('dtype:', mascara.dtype)   # uint8 = 1 byte por píxel → ahorra MUCHA memoria
"""))

A.append(cell("code", """\
# Raster relleno con valor "nodata" típico
nodata_val = -9999
relleno = np.full((4, 4), nodata_val, dtype='int16')
print(relleno)
"""))

A.append(cell("code", """\
# Simulamos una banda Landsat de 5x5 píxeles con reflectancia 0-1
np.random.seed(42)
banda_simulada = np.random.rand(5, 5).round(2)
print(banda_simulada)
"""))

A.append(cell("markdown", """\
---
## 3. Atributos del array → propiedades del raster

Cuando abramos un raster con `rasterio` y pidamos `src.read()`, lo que obtenemos es un **`ndarray`**. Estos atributos serán nuestro pan de cada día:
"""))

A.append(cell("code", """\
# Simulamos un raster multibanda Landsat: (6 bandas, 5 filas, 5 columnas)
np.random.seed(0)
landsat_simulado = np.random.rand(6, 5, 5).astype('float32')

print('ndim:   ', landsat_simulado.ndim,    '→ nº de dimensiones (3 = multibanda)')
print('shape:  ', landsat_simulado.shape,   '→ (bandas, alto, ancho)')
print('size:   ', landsat_simulado.size,    '→ nº total de píxeles × bandas')
print('dtype:  ', landsat_simulado.dtype,   '→ tipo de dato; float32 = 4 bytes/píxel')
print('nbytes: ', landsat_simulado.nbytes,  '→ memoria ocupada en bytes')
"""))

A.append(cell("markdown", """\
> ⚠️ **Importante**: el `dtype` determina el peso del raster. Una Landsat completa en `uint16` (2 bytes) ocupa la mitad que en `float32` (4 bytes). Solo convertimos a float cuando vamos a hacer divisiones (p. ej. al calcular NDVI), si no, se queda en su tipo entero.
"""))

A.append(cell("code", """\
# Convertir tipo de dato (cast). Necesario antes de divisiones para evitar truncamiento entero
entero = np.array([[1, 2], [3, 4]], dtype='uint8')
flotante = entero.astype('float32')
print('Entero:   ', entero, entero.dtype)
print('Flotante: ', flotante, flotante.dtype)

# Si dividimos enteros, perdemos decimales
print('\\nDivisión entera:  ', np.array([1], dtype='uint8') / np.array([3], dtype='uint8'))
# NumPy promueve a float64 automáticamente al dividir, pero si lo hubiéramos hecho con // sí truncaría
"""))

A.append(cell("markdown", """\
---
## 4. Indexación y *slicing*

Slicing en NumPy = recortar una ventana del raster sin abrirlo entero.
"""))

A.append(cell("markdown", """\
![axis](https://courses.spatialthoughts.com/images/python_foundation/pandas_axis.png)

En 2D: `array[fila, columna]`. En 3D: `array[banda, fila, columna]`.
"""))

A.append(cell("code", """\
# Volvemos al mini-raster 3x3
mini_raster = np.array([
    [0.10, 0.12, 0.08],
    [0.45, 0.52, 0.50],
    [0.78, 0.82, 0.80],
])

print('Píxel (0,1):           ', mini_raster[0, 1])
print('Fila 0 entera:         ', mini_raster[0])
print('Columna 1 entera:      ', mini_raster[:, 1])
print('Subraster 2x2 (sup-der):\\n', mini_raster[0:2, 1:3])
"""))

A.append(cell("code", """\
# Recorte de una ventana 3x3 dentro de un raster grande
raster_grande = np.arange(100).reshape(10, 10)
print('Raster 10x10:')
print(raster_grande)

# Ventana centrada en (5,5), tamaño 3x3
ventana = raster_grande[4:7, 4:7]
print('\\nVentana 3x3:')
print(ventana)
"""))

A.append(cell("code", """\
# En un raster multibanda, seleccionar una banda concreta
# landsat_simulado.shape = (6, 5, 5)
banda_NIR = landsat_simulado[3]    # asumimos banda 4 (índice 3) = NIR
print('Forma de la banda NIR:', banda_NIR.shape)
print(banda_NIR)
"""))

A.append(cell("markdown", """\
---
## 5. Álgebra elemento a elemento — la base del NDVI

Las operaciones aritméticas se aplican **píxel a píxel**, sin escribir un solo bucle. Esto es lo que hace posible que un NDVI sobre una imagen entera sea **una sola línea de código**.
"""))

A.append(cell("code", """\
# Simulamos 2 bandas pequeñas (rojo y NIR) de 4x4 píxeles
rojo = np.array([
    [0.05, 0.06, 0.08, 0.10],
    [0.07, 0.04, 0.05, 0.09],
    [0.15, 0.18, 0.20, 0.22],
    [0.30, 0.32, 0.31, 0.30],
], dtype='float32')

nir = np.array([
    [0.05, 0.04, 0.06, 0.08],   # agua (NIR bajo)
    [0.55, 0.52, 0.58, 0.50],   # vegetación sana
    [0.25, 0.28, 0.30, 0.27],   # suelo
    [0.40, 0.45, 0.42, 0.41],   # vegetación moderada
], dtype='float32')

ndvi = (nir - rojo) / (nir + rojo)
print(ndvi.round(2))
"""))

A.append(cell("markdown", """\
**Lee la matriz:** los valores cercanos a 0 son agua, ~0.8 vegetación sana, ~0.3 suelo desnudo o vegetación poco vigorosa.
"""))

A.append(cell("code", """\
# Operadores básicos sobre arrays — todos vectorizados
a = np.array([1.0, 2.0, 3.0])
b = np.array([10.0, 20.0, 30.0])
print('a + b =', a + b)
print('b / a =', b / a)
print('a ** 2 =', a ** 2)
print('-a    =', -a)
"""))

A.append(cell("markdown", """\
---
## 6. Reshape, stack y concatenación — apilar bandas
"""))

A.append(cell("code", """\
# reshape: cambiar la forma sin tocar los datos
v = np.arange(12)
print('Vector original (12,):', v)
print('Reshape a (3,4):\\n', v.reshape(3, 4))
print('Reshape a (2,2,3) — como 2 bandas 2x3:\\n', v.reshape(2, 2, 3))
"""))

A.append(cell("code", """\
# np.stack — apilar bandas en un raster multibanda
banda1 = np.full((3, 3), 1, dtype='uint8')
banda2 = np.full((3, 3), 2, dtype='uint8')
banda3 = np.full((3, 3), 3, dtype='uint8')

# eje 0 → quedan en forma (bandas, alto, ancho) → como rasterio espera
stack = np.stack([banda1, banda2, banda3], axis=0)
print('shape:', stack.shape)
print(stack)
"""))

A.append(cell("code", """\
# np.dstack — apila por el último eje → forma (alto, ancho, bandas)
# Es la forma que espera matplotlib.imshow para mostrar una RGB
rgb = np.dstack([banda1, banda2, banda3])
print('shape:', rgb.shape, '← matplotlib quiere así')
"""))

A.append(cell("markdown", """\
> **A recordar:**
> - **Rasterio** entrega y espera `(bandas, alto, ancho)` → usa `np.stack`.
> - **Matplotlib `imshow`** quiere `(alto, ancho, bandas)` para RGB → usa `np.dstack`.
> - Para pasar entre uno y otro: `np.moveaxis(arr, 0, -1)` o `arr.transpose(1, 2, 0)`.
"""))

A.append(cell("markdown", """\
---
## 7. Funciones universales (ufuncs)

Operan elemento a elemento sobre arrays. Las que más usaremos:
"""))

A.append(cell("code", """\
x = np.array([0.01, 0.1, 1.0, 10.0, 100.0])

print('np.log(x)   =', np.log(x).round(2))    # útil en transformaciones radiométricas
print('np.sqrt(x)  =', np.sqrt(x).round(2))
print('np.abs(-x)  =', np.abs(-x))
print('np.exp([0,1]) =', np.exp([0, 1]).round(3))
"""))

A.append(cell("code", """\
# np.clip — saturar valores en un rango (útil para reflectancias fuera de [0,1] por ruido)
refl = np.array([-0.05, 0.2, 0.7, 1.15, 0.95])
refl_clip = np.clip(refl, 0, 1)
print('Original:', refl)
print('Saturada:', refl_clip)
"""))

A.append(cell("markdown", """\
---
## 8. Estadística por eje

Cuando trabajamos con un *stack* multibanda, `axis` decide si calculamos sobre bandas, filas o columnas.
"""))

A.append(cell("code", """\
# Volvemos a nuestro NDVI 4x4
print('NDVI:')
print(ndvi.round(2))

print('\\nGlobal:')
print(f'  min:    {ndvi.min():.2f}')
print(f'  max:    {ndvi.max():.2f}')
print(f'  media:  {ndvi.mean():.2f}')
print(f'  mediana:{np.median(ndvi):.2f}')
print(f'  std:    {ndvi.std():.2f}')
"""))

A.append(cell("code", """\
# Por filas vs por columnas
print('Media por columna (axis=0):', ndvi.mean(axis=0).round(2))
print('Media por fila    (axis=1):', ndvi.mean(axis=1).round(2))
"""))

A.append(cell("code", """\
# Stack de 3 bandas → media a lo largo del eje de bandas (axis=0)
# Es lo que hacen los compuestos temporales: la media de varias fechas píxel a píxel
stack_temporal = np.stack([
    np.array([[0.3, 0.4], [0.5, 0.6]]),    # primavera
    np.array([[0.7, 0.8], [0.6, 0.5]]),    # verano
    np.array([[0.5, 0.5], [0.4, 0.3]]),    # otoño
])
print('shape:', stack_temporal.shape, '(fechas, alto, ancho)')
print('\\nMedia anual por píxel:\\n', stack_temporal.mean(axis=0).round(2))
print('\\nMáximo anual por píxel (NDVImax):\\n', stack_temporal.max(axis=0).round(2))
"""))

A.append(cell("markdown", """\
> El **NDVI máximo anual** (max compositing) es uno de los compuestos más utilizados — es exactamente `stack.max(axis=0)`.
"""))

A.append(cell("markdown", """\
---
## 9. Máscaras booleanas — el corazón de la teledetección

Una **máscara** es un array de `True`/`False` del mismo tamaño que el raster. Te permite:
- **filtrar** píxeles (`raster[mascara]`)
- **reasignar** valores (`raster[mascara] = nuevo_valor`)
- **contar** (`mascara.sum()` cuenta los `True`)
- **combinar** (`mask1 & mask2`, `mask1 | mask2`, `~mask1`)
"""))

A.append(cell("code", """\
# Máscara de agua a partir de NDVI: agua = NDVI < 0
agua = ndvi < 0
print('Máscara de agua:')
print(agua)
print(f'\\nNº de píxeles de agua: {agua.sum()} de {agua.size}')
"""))

A.append(cell("code", """\
# Filtrar: devuelve un VECTOR con los valores donde la máscara es True
valores_agua = ndvi[agua]
print('Valores NDVI donde hay agua:', valores_agua)
print('Media:', valores_agua.mean().round(3))
"""))

A.append(cell("code", """\
# Reasignar: poner a -9999 todos los píxeles que no son vegetación
ndvi_solo_veg = ndvi.copy()                  # ¡copy! si no, modificarías el original
ndvi_solo_veg[ndvi_solo_veg < 0.3] = -9999
print(ndvi_solo_veg.round(2))
"""))

A.append(cell("code", """\
# Combinar máscaras: vegetación moderada = 0.3 < NDVI <= 0.6
veg_moderada = (ndvi > 0.3) & (ndvi <= 0.6)
print(veg_moderada)
print(f'\\nPíxeles de vegetación moderada: {veg_moderada.sum()}')

# Operadores: & (and), | (or), ~ (not). OJO con los paréntesis.
"""))

A.append(cell("code", """\
# np.where(condición, valor_si_True, valor_si_False) — el "IF" vectorizado
clasif = np.where(ndvi < 0, 0,                       # agua
           np.where(ndvi < 0.3, 1,                   # suelo
            np.where(ndvi < 0.6, 2, 3)))             # veg moderada / sana
print(clasif)
"""))

A.append(cell("markdown", """\
> Este `np.where` anidado es la versión "casera" de una clasificación raster por umbrales. Es exactamente lo que harías en una calculadora de raster de QGIS, pero en una sola línea.
"""))

A.append(cell("markdown", """\
---
## 10. Mini-ejercicios

> **Cómo trabajar los ejercicios:** edita la celda marcada con `# *** TU CÓDIGO AQUÍ ***`. La celda siguiente contiene la solución comentada.
"""))

A.append(cell("markdown", """\
### Ejercicio 1 — NDVI a mano

Calcula el NDVI a partir de las bandas `rojo_e` y `nir_e` que ya tienes definidas. Pista: usa álgebra de bandas y conviértelas a `float32` si no lo están.
"""))

A.append(cell("code", """\
# Datos del ejercicio
rojo_e = np.array([
    [0.05, 0.08, 0.04, 0.06],
    [0.20, 0.22, 0.25, 0.18],
    [0.30, 0.32, 0.35, 0.28],
], dtype='float32')

nir_e = np.array([
    [0.04, 0.06, 0.05, 0.04],   # agua
    [0.55, 0.60, 0.62, 0.50],   # vegetación
    [0.32, 0.34, 0.36, 0.30],   # suelo
], dtype='float32')

# *** TU CÓDIGO AQUÍ ***
ndvi_e = None

print(ndvi_e)
"""))

A.append(cell("code", """\
# SOLUCIÓN — descomenta para ver
# ndvi_e = (nir_e - rojo_e) / (nir_e + rojo_e)
# print(ndvi_e.round(2))
"""))

A.append(cell("markdown", """\
### Ejercicio 2 — Máscara de agua

Crea una máscara booleana `mask_agua` que sea `True` donde el NDVI calculado en el ejercicio anterior es negativo. Cuenta los píxeles de agua.
"""))

A.append(cell("code", """\
# *** TU CÓDIGO AQUÍ ***
mask_agua = None

print(mask_agua)
# print(f'Píxeles de agua: {mask_agua.sum()}')
"""))

A.append(cell("code", """\
# SOLUCIÓN
# mask_agua = ndvi_e < 0
# print(mask_agua)
# print(f'Píxeles de agua: {mask_agua.sum()}')
"""))

A.append(cell("markdown", """\
### Ejercicio 3 — Índice de clorofila CIgreen (proxy)

El índice **Chlorophyll Index green** se calcula como:

$$ CI_{green} = \\frac{NIR}{Green} - 1 $$

Calcúlalo con los siguientes datos. Devuelve una matriz `cigreen`.
"""))

A.append(cell("code", """\
green_e = np.array([
    [0.06, 0.07, 0.06, 0.06],
    [0.08, 0.09, 0.08, 0.08],
    [0.12, 0.13, 0.14, 0.11],
], dtype='float32')

# nir_e ya está definido arriba

# *** TU CÓDIGO AQUÍ ***
cigreen = None

print(cigreen)
"""))

A.append(cell("code", """\
# SOLUCIÓN
# cigreen = nir_e / green_e - 1
# print(cigreen.round(2))
"""))

A.append(cell("markdown", """\
### Ejercicio 4 — Estadística zonal "casera"

Tienes un raster de NDVI `ndvi_grande` (10×10) y una máscara `zona` que marca con `True` los píxeles dentro de un término municipal ficticio. Calcula la media, mínimo y máximo del NDVI **dentro de la zona**.
"""))

A.append(cell("code", """\
np.random.seed(7)
ndvi_grande = (np.random.rand(10, 10) * 1.4 - 0.2).astype('float32')   # rango aprox [-0.2, 1.2]

# zona = un cuadrado en la esquina superior izquierda
zona = np.zeros_like(ndvi_grande, dtype=bool)
zona[1:5, 1:6] = True

print('NDVI:')
print(ndvi_grande.round(2))
print('\\nZona (True = dentro):')
print(zona.astype(int))
"""))

A.append(cell("code", """\
# *** TU CÓDIGO AQUÍ ***
# Calcula media, min y max del NDVI dentro de la zona
media_zona = None
min_zona   = None
max_zona   = None

# print(f'media={media_zona:.2f} | min={min_zona:.2f} | max={max_zona:.2f}')
"""))

A.append(cell("code", """\
# SOLUCIÓN
# valores = ndvi_grande[zona]
# media_zona = valores.mean()
# min_zona   = valores.min()
# max_zona   = valores.max()
# print(f'media={media_zona:.2f} | min={min_zona:.2f} | max={max_zona:.2f}')
"""))

A.append(cell("markdown", """\
---
## Resumen

| Concepto | Lo clave |
|----------|----------|
| **Crear** | `np.array`, `np.zeros`, `np.ones`, `np.full`, `np.random.rand` |
| **Atributos** | `.shape`, `.ndim`, `.dtype`, `.size`, `.nbytes` |
| **Tipo** | `.astype('float32')` antes de dividir; `uint8` para máscaras |
| **Slicing** | `a[fila, col]`, `a[banda, fila, col]`, `a[i:j, k:l]` |
| **Álgebra** | `(nir - red) / (nir + red)` → vectorizado, sin bucles |
| **Apilar** | `np.stack` (bandas-alto-ancho) · `np.dstack` (alto-ancho-bandas) |
| **Stats por eje** | `arr.mean(axis=0)`, `arr.max(axis=0)` → compuestos temporales |
| **Máscaras** | `mask = arr > umbral`; `arr[mask]`; `mask1 & mask2`; `~mask` |
| **`np.where`** | El "IF" vectorizado para clasificar |

**Siguiente notebook:** abrimos una imagen Landsat real sobre Doñana con `rasterio` y aplicamos todo esto.

---
*CHG — Curso de Python para el Análisis Espacial*
"""))

write_nb("03a_intro_numpy.ipynb", A)


# =====================================================================
# 03b — Rasterio: lectura, índices, máscaras, poligonización, zonal
# =====================================================================
B = []

B.append(cell("markdown", """\
# CHG — Análisis Raster con Python
## Día 3 · Módulo B: Rasterio — Landsat sobre Doñana

**Curso de Python para el Análisis Espacial**
Confederación Hidrográfica del Guadalquivir

---

En este notebook usaremos una **imagen Landsat 8/9 recortada sobre Doñana y el bajo Guadalquivir**, ya reescalada a reflectancia (valores 0–1, `float32`), con 6 bandas en este orden:

| Índice (Python) | Banda     | λ (µm)      | Para qué |
|-----------------|-----------|-------------|----------|
| `1`             | Blue  (B2)| 0.45–0.51   | Composiciones color natural |
| `2`             | Green (B3)| 0.53–0.59   | NDWI, color natural |
| `3`             | Red   (B4)| 0.64–0.67   | NDVI, color natural |
| `4`             | NIR   (B5)| 0.85–0.88   | NDVI, NDWI, biomasa |
| `5`             | SWIR1 (B6)| 1.57–1.65   | MNDWI, humedad |
| `6`             | SWIR2 (B7)| 2.11–2.29   | Falsos color, geología |

> Rasterio numera las bandas **empezando por 1** (no por 0), porque internamente usa GDAL.

## Contenidos

1. Setup en Colab (descarga desde Nextcloud) o local
2. **GDAL bajo el capó** — `gdalinfo`, `gdal_translate`, `gdalwarp`
3. Abrir el raster: `crs`, `transform`, `bounds`, `profile`
4. Leer bandas — una a una y *stack* completo
5. Visualización banda a banda y composiciones RGB
6. Álgebra de bandas: **NDVI**, **NDWI**, **MNDWI**, **CIgreen**
7. Guardar un raster derivado a disco
8. **Máscara de agua** → **poligonización** con `rasterio.features.shapes()`
9. Recorte de raster por un vectorial (`rasterio.mask.mask`)
10. **Estadísticas zonales** con `rasterstats`
11. Ejercicio final integrador
12. Apéndice: cómo se preparó el recorte Landsat
"""))

B.append(cell("markdown", """\
---
## 1. Setup — datos en Colab o en local

Este notebook está pensado para ejecutarse **tanto en Colab como en local**. La celda siguiente detecta el entorno:
- Si estás en **Colab**, descarga la imagen Landsat y los vectoriales desde Nextcloud.
- Si estás en **local**, asume que los vectoriales viven en `../dia_2_analisis_vectorial/data/` y la Landsat en `./data/`.

> ✏️ **Profesor: sustituir las URL `NEXTCLOUD_…` por los enlaces compartidos reales antes de la clase.**
"""))

B.append(cell("code", '''\
import os, sys, subprocess, pathlib

# --- URLs Nextcloud (rellenar con los enlaces públicos /download de cada archivo) ---
NEXTCLOUD_LANDSAT      = "https://nextcloud.tu-dominio.es/s/REEMPLAZAR_LANDSAT/download"
NEXTCLOUD_MUNICIPIOS   = "https://nextcloud.tu-dominio.es/s/REEMPLAZAR_MUNICIPIOS/download"
NEXTCLOUD_CUENCAS      = "https://nextcloud.tu-dominio.es/s/REEMPLAZAR_CUENCAS/download"
NEXTCLOUD_EMBALSES     = "https://nextcloud.tu-dominio.es/s/REEMPLAZAR_EMBALSES/download"

try:
    import google.colab  # noqa
    EN_COLAB = True
except ImportError:
    EN_COLAB = False

if EN_COLAB:
    # Instalación de dependencias geoespaciales no incluidas por defecto en Colab
    subprocess.run(["pip", "-q", "install", "rasterio", "rasterstats", "geopandas", "matplotlib"], check=False)

    def _fetch(url, dst):
        if not os.path.exists(dst):
            print(f"⬇️  Descargando {dst}…")
            subprocess.run(["wget", "-q", "-O", dst, url], check=True)
        else:
            print(f"✔  {dst} ya está descargado")

    _fetch(NEXTCLOUD_LANDSAT,    "landsat_donana.tif")
    _fetch(NEXTCLOUD_MUNICIPIOS, "terminos_municipales_andalucia.gpkg")
    _fetch(NEXTCLOUD_CUENCAS,    "cuencas_guadalquivir.gpkg")
    _fetch(NEXTCLOUD_EMBALSES,   "embalses_guadalquivir.gpkg")

    LANDSAT_PATH  = "landsat_donana.tif"
    MUNICIPIOS    = "terminos_municipales_andalucia.gpkg"
    CUENCAS       = "cuencas_guadalquivir.gpkg"
    EMBALSES      = "embalses_guadalquivir.gpkg"
else:
    DATA_VECT = pathlib.Path("../dia_2_analisis_vectorial/data")
    DATA_RAST = pathlib.Path("./data")
    LANDSAT_PATH  = str(DATA_RAST / "landsat_donana.tif")
    MUNICIPIOS    = str(DATA_VECT / "terminos_municipales_andalucia.gpkg")
    CUENCAS       = str(DATA_VECT / "cuencas_guadalquivir.gpkg")
    EMBALSES      = str(DATA_VECT / "embalses_guadalquivir.gpkg")

print("Entorno:", "Colab" if EN_COLAB else "Local")
print("Raster: ", LANDSAT_PATH, "→ existe:", os.path.exists(LANDSAT_PATH))
'''))

B.append(cell("code", """\
import numpy as np
import matplotlib.pyplot as plt
import rasterio
from rasterio.plot import show
import geopandas as gpd

print(f'rasterio {rasterio.__version__}')
print(f'geopandas {gpd.__version__}')
"""))

B.append(cell("markdown", """\
---
## 2. GDAL — el motor que hay debajo

Antes de tirar de `rasterio`, una breve pausa para ver qué hay realmente bajo el capó.

**GDAL** (Geospatial Data Abstraction Library) es una librería C/C++ de los años 90 que sabe leer, escribir y transformar **más de 160 formatos raster** (y otros tantos vectoriales). Es la base sobre la que se apoyan casi todas las herramientas SIG modernas:

```
            GDAL  (C/C++, formato + álgebra + reproyección)
              │
   ┌──────────┼──────────────────────────────────────┐
   │          │                                      │
  QGIS    rasterio (Python)                  GRASS, SAGA, ArcGIS,
          rioxarray, fiona, gdalwarp,        Google Earth Engine,
          osgeo.gdal …                       PostGIS raster, ...
```

GDAL viene **preinstalado en Colab** (paquete `gdal-bin`). Podemos llamarlo desde el notebook con el prefijo `!`.
"""))

B.append(cell("code", "!gdalinfo --version"))

B.append(cell("markdown", """\
### `gdalinfo` — el "describir" del raster

Equivale a abrirlo con rasterio y consultar `.crs`, `.bounds`, `.transform`, estadísticas… todo de un golpe.
"""))

B.append(cell("code", "!gdalinfo {LANDSAT_PATH}"))

B.append(cell("markdown", """\
> Lo que ves aquí es exactamente lo mismo que rasterio expone en `.profile`, `.bounds`, `.transform`, etc. La diferencia: rasterio te lo da como objetos Python manejables.
"""))

B.append(cell("markdown", """\
### `gdal_translate` — convertir / recortar / extraer bandas

Algunos ejemplos clásicos (sustituye `!` por terminal fuera de Jupyter):
"""))

B.append(cell("code", """\
# Extraer SOLO la banda 4 (NIR) a un fichero nuevo, comprimido
!gdal_translate -b 4 -co COMPRESS=DEFLATE -co TILED=YES \\
    {LANDSAT_PATH} solo_nir.tif

# Pedimos a GDAL que nos informe del resultado
!gdalinfo solo_nir.tif | head -15
"""))

B.append(cell("markdown", """\
### `gdalwarp` — reproyectar y/o recortar

Reproyectar a coordenadas geográficas (WGS84) — útil para visualizar en folium/leaflet sin pasar por Python:

```bash
gdalwarp -t_srs EPSG:4326 -r bilinear  landsat_donana.tif  landsat_wgs84.tif
```

Recortar por un vectorial (lo mismo que `rasterio.mask.mask`, pero en CLI):

```bash
gdalwarp -cutline almonte.gpkg -crop_to_cutline  landsat_donana.tif  landsat_almonte.tif
```

### Cuándo GDAL CLI y cuándo rasterio

| Tarea | Mejor con |
|-------|-----------|
| Inspección rápida de un fichero | `gdalinfo` |
| Conversión de formato puntual | `gdal_translate` |
| Reproyectar/recortar en *batch* (scripts shell, automatización en CI) | `gdalwarp` |
| Cualquier análisis donde mezclas datos con código Python | `rasterio` |
| Acceder al array NumPy del raster para hacer álgebra | `rasterio` |
| Integrarlo con pandas/geopandas en un workflow | `rasterio` |

> Resumen: **rasterio = GDAL con cara de Python**. Saber que GDAL existe te abre la puerta a leer documentación, copiar comandos de Stack Overflow y entender cualquier librería raster del ecosistema.
"""))

B.append(cell("markdown", """\
---
## 3. Abrir el raster y leer sus metadatos

`rasterio.open()` no carga los píxeles en memoria — solo los metadatos. Esto te permite consultar el CRS, la resolución y los bounds **sin coste**, antes de decidir cuánto leer.
"""))

B.append(cell("code", """\
src = rasterio.open(LANDSAT_PATH)
print('CRS:       ', src.crs)
print('Bounds:    ', src.bounds)
print('Width x H: ', src.width, 'x', src.height)
print('Bandas:    ', src.count)
print('Dtype:     ', src.dtypes[0])
print('NoData:    ', src.nodatavals)
print('Transform: ', src.transform)
"""))

B.append(cell("markdown", """\
### El `Affine` transform

```
Affine(a, b, c,
       d, e, f)
```

- `a` = tamaño de píxel en X (resolución horizontal, m si el CRS es proyectado)
- `e` = tamaño de píxel en Y (negativo, porque los rasters se almacenan de arriba abajo)
- `c`, `f` = coordenadas del píxel superior izquierdo

Con esto, rasterio convierte fila/columna a coordenadas del mundo (y viceversa).
"""))

B.append(cell("code", """\
# Coordenadas del píxel central
fila_c, col_c = src.height // 2, src.width // 2
x, y = src.transform * (col_c, fila_c)
print(f'Píxel central (col={col_c}, fila={fila_c}) → ({x:.1f}, {y:.1f}) en {src.crs}')

# Y al revés
fila, col = src.index(x, y)
print(f'Coords ({x:.1f}, {y:.1f}) → píxel (col={col}, fila={fila})')
"""))

B.append(cell("code", """\
# El profile: el "carnet de identidad" del raster. Lo reutilizaremos al escribir derivados.
profile = src.profile
print(profile)
"""))

B.append(cell("markdown", """\
---
## 4. Leer bandas

Tres formas:
1. `src.read(n)` → numpy 2D de la banda `n`.
2. `src.read([1,2,3])` → numpy 3D con varias bandas en orden.
3. `src.read()` → numpy 3D con **todas** las bandas. Forma `(bandas, alto, ancho)`.
"""))

B.append(cell("code", """\
red   = src.read(3)
nir   = src.read(4)
green = src.read(2)
swir1 = src.read(5)

print('NIR shape:', nir.shape, '| dtype:', nir.dtype)
print(f'NIR  rango: {nir.min():.3f} – {nir.max():.3f}')
print(f'Red  rango: {red.min():.3f} – {red.max():.3f}')
"""))

B.append(cell("code", """\
# Stack completo de las 6 bandas en una sola llamada
stack = src.read()       # shape (6, H, W)
print('Stack shape:', stack.shape)
print('Memoria:    {:.1f} MB'.format(stack.nbytes / 1e6))
"""))

B.append(cell("markdown", """\
---
## 5. Visualización

### 5.1 Una banda con su colormap
"""))

B.append(cell("code", """\
fig, ax = plt.subplots(figsize=(8, 8))
img = ax.imshow(nir, cmap='gray', vmin=0, vmax=0.5)
plt.colorbar(img, ax=ax, fraction=0.04, label='Reflectancia NIR')
ax.set_title('Banda NIR (B5) — Landsat sobre Doñana')
ax.set_axis_off()
plt.show()
"""))

B.append(cell("markdown", """\
### 5.2 Las 6 bandas a la vez
"""))

B.append(cell("code", """\
nombres = ['Blue (B2)', 'Green (B3)', 'Red (B4)', 'NIR (B5)', 'SWIR1 (B6)', 'SWIR2 (B7)']

fig, axes = plt.subplots(2, 3, figsize=(15, 9))
for i, ax in enumerate(axes.flat):
    banda = stack[i]
    # vmax por percentil para evitar que un píxel saturado nos coma el contraste
    vmax = np.percentile(banda, 98)
    ax.imshow(banda, cmap='gray', vmin=0, vmax=vmax)
    ax.set_title(nombres[i])
    ax.set_axis_off()
plt.tight_layout()
plt.show()
"""))

B.append(cell("markdown", """\
### 5.3 Composición color natural (RGB)

Para que matplotlib muestre una RGB necesita:
- forma `(alto, ancho, 3)` → usamos `np.dstack`
- valores en `[0, 1]` → recortamos y/o estiramos contraste
"""))

B.append(cell("code", """\
def estirar(banda, p_min=2, p_max=98):
    \"\"\"Estiramiento lineal por percentiles para realzar el contraste visual.\"\"\"
    vmin, vmax = np.percentile(banda, [p_min, p_max])
    return np.clip((banda - vmin) / (vmax - vmin), 0, 1)

rgb_natural = np.dstack([
    estirar(red),    # R
    estirar(green),  # G
    estirar(src.read(1)),  # B (blue)
])

fig, ax = plt.subplots(figsize=(9, 9))
ax.imshow(rgb_natural)
ax.set_title('Color natural (R=B4, G=B3, B=B2) — Doñana')
ax.set_axis_off()
plt.show()
"""))

B.append(cell("markdown", """\
### 5.4 Falso color infrarrojo — la vegetación en rojo

Sustituir el rojo visible por el NIR resalta toda la vegetación viva en tonos rojos. Es el "clásico" de la teledetección.
"""))

B.append(cell("code", """\
rgb_falso = np.dstack([
    estirar(nir),     # R ← NIR
    estirar(red),     # G ← Red
    estirar(green),   # B ← Green
])

fig, ax = plt.subplots(figsize=(9, 9))
ax.imshow(rgb_falso)
ax.set_title('Falso color IR (R=NIR, G=Red, B=Green) — vegetación en rojo')
ax.set_axis_off()
plt.show()
"""))

B.append(cell("markdown", """\
---
## 6. Álgebra de bandas — los índices clásicos

### 6.1 NDVI — vigor vegetal

$$NDVI = \\dfrac{NIR - Red}{NIR + Red}$$

Rango teórico [-1, 1]. Vegetación sana ~0.6–0.9, suelo ~0.1–0.3, agua ~0 o negativo.

> Antes de dividir, **siempre** convertir a `float`. Si las bandas vienen como `uint16` la división trunca a entero.
"""))

B.append(cell("code", """\
# np.errstate suprime el warning de "división por cero" en píxeles nodata
with np.errstate(divide='ignore', invalid='ignore'):
    ndvi = (nir - red) / (nir + red)

print(f'NDVI rango: {np.nanmin(ndvi):.2f} – {np.nanmax(ndvi):.2f}')
print(f'NDVI media: {np.nanmean(ndvi):.2f}')
"""))

B.append(cell("code", """\
fig, ax = plt.subplots(figsize=(9, 9))
img = ax.imshow(ndvi, cmap='RdYlGn', vmin=-0.2, vmax=0.8)
plt.colorbar(img, ax=ax, fraction=0.04, label='NDVI')
ax.set_title('NDVI — Doñana')
ax.set_axis_off()
plt.show()
"""))

B.append(cell("markdown", """\
### 6.2 NDWI de McFeeters (1996) — detecta agua

$$NDWI = \\dfrac{Green - NIR}{Green + NIR}$$

Agua → positivo. Vegetación y suelo → negativo. Es el clásico para masas de agua claras.
"""))

B.append(cell("code", """\
with np.errstate(divide='ignore', invalid='ignore'):
    ndwi = (green - nir) / (green + nir)

fig, ax = plt.subplots(figsize=(9, 9))
img = ax.imshow(ndwi, cmap='Blues', vmin=-0.3, vmax=0.6)
plt.colorbar(img, ax=ax, fraction=0.04, label='NDWI')
ax.set_title('NDWI (McFeeters) — Doñana')
ax.set_axis_off()
plt.show()
"""))

B.append(cell("markdown", """\
### 6.3 MNDWI de Xu (2006) — agua mejor en zonas urbanas/turbias

$$MNDWI = \\dfrac{Green - SWIR_1}{Green + SWIR_1}$$

El SWIR es **muy** absorbido por el agua, así que el contraste agua/no-agua es mayor que en NDWI. Es el índice preferido para marismas, aguas someras y cuerpos urbanos.
"""))

B.append(cell("code", """\
with np.errstate(divide='ignore', invalid='ignore'):
    mndwi = (green - swir1) / (green + swir1)

fig, axes = plt.subplots(1, 2, figsize=(15, 7))
axes[0].imshow(ndwi, cmap='Blues', vmin=-0.3, vmax=0.6)
axes[0].set_title('NDWI (McFeeters)')
axes[0].set_axis_off()

im = axes[1].imshow(mndwi, cmap='Blues', vmin=-0.3, vmax=0.8)
axes[1].set_title('MNDWI (Xu) — mejor para marismas')
axes[1].set_axis_off()
plt.colorbar(im, ax=axes[1], fraction=0.04)
plt.tight_layout()
plt.show()
"""))

B.append(cell("markdown", """\
### 6.4 CIgreen — proxy de clorofila

$$CI_{green} = \\dfrac{NIR}{Green} - 1$$

Muy correlacionado con el contenido de clorofila en hoja. Útil para seguimiento de cultivos y, también, para detectar **blooms de fitoplancton/algas** en láminas de agua.
"""))

B.append(cell("code", """\
with np.errstate(divide='ignore', invalid='ignore'):
    cigreen = nir / green - 1

fig, ax = plt.subplots(figsize=(9, 9))
img = ax.imshow(cigreen, cmap='YlGn', vmin=0, vmax=8)
plt.colorbar(img, ax=ax, fraction=0.04, label='CIgreen')
ax.set_title('Chlorophyll Index green — Doñana')
ax.set_axis_off()
plt.show()
"""))

B.append(cell("markdown", """\
---
## 7. Guardar un raster derivado

Para escribir un GeoTIFF nuevo necesitamos un **`profile`** (los metadatos que describen el archivo). Lo más cómodo es **partir del profile original** y modificar lo que cambie: el número de bandas y el `dtype`.
"""))

B.append(cell("code", """\
profile_ndvi = src.profile.copy()
profile_ndvi.update(
    count=1,            # 1 sola banda
    dtype='float32',    # NDVI es float
    nodata=np.nan,      # marcamos NoData como NaN
    compress='deflate',
)

with rasterio.open('ndvi_donana.tif', 'w', **profile_ndvi) as dst:
    dst.write(ndvi.astype('float32'), 1)
    dst.set_band_description(1, 'NDVI')

import os
print(f'Guardado: ndvi_donana.tif ({os.path.getsize(\"ndvi_donana.tif\")/1e6:.1f} MB)')
"""))

B.append(cell("markdown", """\
---
## 8. Máscara de agua → polígonos

Vamos a:
1. Crear una **máscara binaria** de agua con un umbral sobre el MNDWI.
2. **Poligonizarla** con `rasterio.features.shapes()` para obtener un GeoDataFrame de masas de agua.

Esto es lo que QGIS llama "Raster → Vectorial (Poligonizar)" — pero en Python, en una celda.
"""))

B.append(cell("code", """\
# Umbral típico: MNDWI > 0 → agua. Subimos un poco para ser más conservadores.
UMBRAL = 0.1
mask_agua = (mndwi > UMBRAL).astype('uint8')   # uint8 — necesario para shapes()

print(f'Píxeles de agua: {mask_agua.sum():,} de {mask_agua.size:,} '
      f'({100*mask_agua.sum()/mask_agua.size:.1f}%)')

fig, ax = plt.subplots(figsize=(9, 9))
ax.imshow(mask_agua, cmap='Blues', vmin=0, vmax=1)
ax.set_title(f'Máscara binaria de agua (MNDWI > {UMBRAL})')
ax.set_axis_off()
plt.show()
"""))

B.append(cell("markdown", """\
### Poligonización con `rasterio.features.shapes`

Genera un iterador `(geometría, valor)` por cada **región conectada** del raster. Filtramos quedándonos solo con `valor == 1` (agua).
"""))

B.append(cell("code", """\
from rasterio.features import shapes
from shapely.geometry import shape

geoms_agua = []
for geom_dict, val in shapes(mask_agua, mask=(mask_agua == 1), transform=src.transform):
    geoms_agua.append({'geometry': shape(geom_dict), 'mndwi_mean': None})

gdf_agua = gpd.GeoDataFrame(geoms_agua, crs=src.crs)
print(f'{len(gdf_agua)} polígonos de agua detectados')

# Filtrar polígonos pequeños (ruido, píxeles aislados)
MIN_AREA_M2 = 30 * 30 * 10   # al menos 10 píxeles Landsat (≈ 0.9 ha)
gdf_agua = gdf_agua[gdf_agua.area > MIN_AREA_M2].reset_index(drop=True)
gdf_agua['area_ha'] = gdf_agua.area / 1e4

print(f'Tras filtrar < {MIN_AREA_M2/1e4:.1f} ha: {len(gdf_agua)} polígonos')
gdf_agua.sort_values('area_ha', ascending=False).head(10)
"""))

B.append(cell("code", """\
# Visualización: polígonos de agua sobre el MNDWI
fig, ax = plt.subplots(figsize=(9, 9))
show(mndwi, transform=src.transform, ax=ax, cmap='Blues', vmin=-0.2, vmax=0.6)
gdf_agua.plot(ax=ax, facecolor='none', edgecolor='red', linewidth=0.7)
ax.set_title(f'Cuerpos de agua detectados ({len(gdf_agua)} polígonos)')
plt.show()
"""))

B.append(cell("code", """\
# Guardar como GeoPackage
gdf_agua.to_file('cuerpos_agua_donana.gpkg', driver='GPKG')
print('Guardado: cuerpos_agua_donana.gpkg')
"""))

B.append(cell("markdown", """\
---
## 9. Recortar el raster por un vectorial

`rasterio.mask.mask(src, geometrias, crop=True)` recorta el raster a la extensión de las geometrías y pone a NoData fuera de ellas.

Aquí recortamos por el **término municipal de Almonte** (Doñana cae mayormente sobre Almonte).
"""))

B.append(cell("code", """\
from rasterio.mask import mask as rio_mask

municipios = gpd.read_file(MUNICIPIOS)
print('CRS municipios:', municipios.crs, '|  CRS raster:', src.crs)

# Reproyectamos los municipios al CRS del raster
municipios = municipios.to_crs(src.crs)

# Filtramos Almonte
almonte = municipios[municipios['nombre'] == 'Almonte']
print(f'Almonte: {len(almonte)} entidad(es), área {almonte.area.iloc[0]/1e6:.1f} km²')
"""))

B.append(cell("code", """\
geom_almonte = [almonte.geometry.iloc[0].__geo_interface__]

with rasterio.open(LANDSAT_PATH) as s:
    img_recortada, t_recortada = rio_mask(s, geom_almonte, crop=True, nodata=np.nan, filled=True)
    prof_rec = s.profile.copy()

prof_rec.update({
    'height':    img_recortada.shape[1],
    'width':     img_recortada.shape[2],
    'transform': t_recortada,
    'dtype':     'float32',
    'nodata':    np.nan,
    'compress':  'deflate',
})

with rasterio.open('landsat_almonte.tif', 'w', **prof_rec) as dst:
    dst.write(img_recortada.astype('float32'))

print('shape recortada:', img_recortada.shape)
print('Guardado: landsat_almonte.tif')
"""))

B.append(cell("code", """\
# NDVI sobre el recorte de Almonte
red_a = img_recortada[2]
nir_a = img_recortada[3]
with np.errstate(divide='ignore', invalid='ignore'):
    ndvi_almonte = (nir_a - red_a) / (nir_a + red_a)

fig, ax = plt.subplots(figsize=(9, 9))
show(ndvi_almonte, transform=t_recortada, ax=ax, cmap='RdYlGn', vmin=-0.2, vmax=0.8)
almonte.boundary.plot(ax=ax, color='black', linewidth=1.2)
ax.set_title('NDVI — Término municipal de Almonte')
plt.show()
"""))

B.append(cell("markdown", """\
---
## 10. Estadísticas zonales — NDVI medio por municipio

`rasterstats` calcula estadísticas de un raster dentro de cada polígono de un vectorial. Ideal para informes tipo "NDVI medio por término municipal" o "lámina de agua por embalse".
"""))

B.append(cell("code", """\
from rasterstats import zonal_stats

# Nos quedamos con los municipios que intersectan el extent del raster, así no perdemos tiempo
from shapely.geometry import box
bbox = box(*src.bounds)
muni_aoi = municipios[municipios.intersects(bbox)].copy()
print(f'{len(muni_aoi)} municipios intersectan el extent del raster')
"""))

B.append(cell("code", """\
stats = zonal_stats(
    muni_aoi,
    'ndvi_donana.tif',          # el raster derivado que guardamos antes
    stats=['mean', 'min', 'max', 'std', 'count'],
    nodata=np.nan,
)

import pandas as pd
muni_aoi = muni_aoi.reset_index(drop=True)
muni_aoi[['ndvi_mean', 'ndvi_min', 'ndvi_max', 'ndvi_std', 'n_pix']] = pd.DataFrame(stats)[
    ['mean', 'min', 'max', 'std', 'count']
]
muni_aoi.sort_values('ndvi_mean', ascending=False)[
    ['nombre', 'provincia', 'ndvi_mean', 'ndvi_std', 'n_pix']
].head(15)
"""))

B.append(cell("code", """\
# Mapa coroplético: NDVI medio por municipio
fig, ax = plt.subplots(figsize=(11, 10))
muni_aoi.plot(column='ndvi_mean', ax=ax, cmap='RdYlGn', legend=True,
              legend_kwds={'label': 'NDVI medio', 'shrink': 0.6},
              edgecolor='gray', linewidth=0.3)
ax.set_title('NDVI medio por término municipal — área Doñana')
ax.set_axis_off()
plt.show()
"""))

B.append(cell("markdown", """\
> **Lectura crítica:** la fecha de la imagen condiciona enormemente el resultado. En invierno, los arrozales de Isla Mayor / La Puebla del Río salen con NDVI bajo (inundados o tierra desnuda) y en verano altísimo. Antes de comparar municipios, **siempre** ojea la fecha del satélite y el calendario de cultivos.
"""))

B.append(cell("markdown", """\
---
## 11. Ejercicio final integrador

Vas a calcular **el área inundada (en hectáreas) dentro del término municipal de Aznalcázar** (cubre buena parte de la marisma sur de Doñana). Pasos:

1. Filtra el GeoDataFrame `municipios` para quedarte con Aznalcázar.
2. Cruza el GeoDataFrame `gdf_agua` (polígonos de agua que ya calculamos) con Aznalcázar — usa `gpd.overlay(..., how='intersection')` o un `clip`.
3. Calcula el área total en hectáreas.
4. Pinta un mapa: el municipio en gris, los polígonos de agua dentro en azul.
"""))

B.append(cell("code", """\
# *** TU CÓDIGO AQUÍ ***
# 1) aznalcazar = ...
# 2) agua_en_aznalcazar = ...
# 3) area_ha = ...
# 4) plot
"""))

B.append(cell("code", """\
# SOLUCIÓN — descomenta para verla
# aznalcazar = municipios[municipios['nombre'] == 'Aznalcázar']
# agua_en_aznalcazar = gpd.overlay(gdf_agua, aznalcazar, how='intersection')
# area_ha = agua_en_aznalcazar.area.sum() / 1e4
# print(f'Área inundada en Aznalcázar: {area_ha:.1f} ha')
#
# fig, ax = plt.subplots(figsize=(9, 9))
# aznalcazar.plot(ax=ax, color='lightgray', edgecolor='black')
# agua_en_aznalcazar.plot(ax=ax, color='steelblue', edgecolor='navy', linewidth=0.5)
# ax.set_title(f'Agua detectada en Aznalcázar: {area_ha:.0f} ha')
# ax.set_axis_off()
# plt.show()
"""))

B.append(cell("markdown", """\
---
## 12. Apéndice — Cómo preparamos la escena Landsat

> Este código **no se ejecuta en clase**, pero se incluye como referencia: enseña cómo se construyó el GeoTIFF multibanda `landsat_donana.tif` a partir de las bandas SR originales de USGS.

```python
import glob, os
import rasterio
from rasterio.mask import mask
import geopandas as gpd

# 1. Bandas SR de Landsat 8/9 L2 — orden Blue, Green, Red, NIR, SWIR1, SWIR2
escena_dir = '/ruta/a/LC08_L2SP_XXX_YYYYMMDD_..._02_T1'
bandas_id  = ['B2', 'B3', 'B4', 'B5', 'B6', 'B7']
paths = [glob.glob(os.path.join(escena_dir, f'*SR_{b}.TIF'))[0] for b in bandas_id]

# 2. Área de interés (Doñana / bajo Guadalquivir)
aoi = gpd.read_file('terminos_municipales_andalucia.gpkg')
aoi = aoi[aoi['nombre'].isin([
    'Almonte', 'Aznalcázar', 'Hinojos', 'Isla Mayor',
    'La Puebla del Río', 'Sanlúcar de Barrameda', 'Lebrija',
])].dissolve()

with rasterio.open(paths[0]) as ref:
    aoi = aoi.to_crs(ref.crs)
geom = [aoi.geometry.iloc[0].__geo_interface__]

# 3. Recortar, reescalar a reflectancia y apilar
stack = []
for p in paths:
    with rasterio.open(p) as s:
        img, tr = mask(s, geom, crop=True)
        # USGS L2 SR: reflectancia = DN * 0.0000275 - 0.2 (Collection 2)
        refl = img[0].astype('float32') * 0.0000275 - 0.2
        stack.append(refl)
        profile = s.profile

profile.update(
    count=len(stack), dtype='float32', transform=tr,
    height=stack[0].shape[0], width=stack[0].shape[1],
    compress='deflate', tiled=True, blockxsize=256, blockysize=256,
    nodata=None,
)

with rasterio.open('landsat_donana.tif', 'w', **profile) as dst:
    for i, banda in enumerate(stack, 1):
        dst.write(banda, i)
        dst.set_band_description(i, bandas_id[i-1])
```

---

## Resumen del día

| Bloque | Función clave |
|--------|---------------|
| Abrir / metadatos | `rasterio.open(path)`, `.crs`, `.transform`, `.bounds`, `.profile` |
| Leer | `.read(n)`, `.read([1,2,3])`, `.read()` |
| Álgebra de bandas | aritmética NumPy elemento a elemento |
| Visualizar | `plt.imshow`, `rasterio.plot.show`, `np.dstack` para RGB |
| Guardar | `rasterio.open(..., 'w', **profile)` |
| Recortar por vectorial | `rasterio.mask.mask(src, geom, crop=True)` |
| Raster → vectorial | `rasterio.features.shapes(mask, transform=...)` |
| Estadísticas zonales | `rasterstats.zonal_stats(vector, raster, stats=[...])` |

---
*CHG — Curso de Python para el Análisis Espacial*
"""))

write_nb("03b_rasterio_indices_mascaras.ipynb", B)

