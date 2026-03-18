# Ejercicio: Comparación de índices FAI/FGAI en embalses del Guadalquivir

## Objetivo

Evaluar el efecto del nivel de corrección atmosférica y la resolución espacial en la detección de floraciones de cianobacterias, calculando los índices FAI/FGAI sobre tres fuentes de datos distintas y comparando los resultados.

## Datos necesarios

| Producto | Nivel | Fecha | Bandas necesarias |
|----------|-------|-------|-------------------|
| Sentinel-2 MSI | L1C | 31/07/2025 | B2, B3, B4, B8 |
| Sentinel-2 MSI | L2A | 31/07/2025 | B4, B8A, B11 |
| Sentinel-3 OLCI | OL_1_EFR | 31/07/2025 | Oa04, Oa06, Oa08, Oa17 |

**Shapefile:** polígonos de los embalses candidatos (Bornos, Guadalcacín, Torre del Águila, Barbate)

**Descarga:** https://dataspace.copernicus.eu/

---

## Escenario 1 — FGAI sobre Sentinel-2 L1C (sin corrección atmosférica)

### 1.1 Abrir el producto
- `File → Open Product` → seleccionar `MTD_MSIL1C.xml`

### 1.2 Subset espacial y de bandas
- `Raster → Subset`
- Pestaña **Spatial Subset** → `Use Shape File...` → cargar el shapefile de embalses
- Pestaña **Band Subset** → seleccionar únicamente: **B2, B3, B4, B8**
- Guardar el subset en disco

### 1.3 Homogeneizar resolución
Las bandas de S2 L1C pueden presentar ligeras diferencias de tamaño en píxeles tras el subset. Para resolverlo:
- `Raster → Geometric → Resample`
- Referencia: **B4**
- Aplicar a todas las bandas

### 1.4 Calcular el FGAI
- `Raster → Band Maths`
- Nombre de la nueva banda: `FGAI_L1C`
- Desmarcar **Virtual Band**
- Expresión:

```
-0.42 * B2 + (-0.15) * B3 + (-0.49) * B4 + 0.75 * B8
```

### 1.5 Exportar
- `File → Export → GeoTIFF`
- Exportar solo la banda `FGAI_L1C`

---

## Escenario 2 — FAI sobre Sentinel-2 L2A (corrección atmosférica completa)

### 2.1 Abrir el producto
- `File → Open Product` → seleccionar `MTD_MSIL2A.xml`

### 2.2 Subset espacial y de bandas
- `Raster → Subset`
- Pestaña **Spatial Subset** → `Use Shape File...` → cargar el shapefile de embalses
- Pestaña **Band Subset** → seleccionar únicamente: **B4 (10 m), B8A (20 m), B11 (20 m)**
- Guardar el subset en disco

### 2.3 Homogeneizar resolución
B4 está a 10 m y B8A/B11 a 20 m — es necesario remuestrear antes del Band Maths:
- `Raster → Geometric → Resample`
- Referencia: **B8A** (20 m) — así todo queda a 20 m
- Aplicar a todas las bandas

### 2.4 Calcular el FAI
- `Raster → Band Maths`
- Nombre de la nueva banda: `FAI_L2A`
- Desmarcar **Virtual Band**
- Expresión:

```
B8A - (B4 + (B11 - B4) * (865.0 - 665.0) / (1610.0 - 665.0))
```

### 2.5 Exportar
- `File → Export → GeoTIFF`
- Exportar solo la banda `FAI_L2A`

---

## Escenario 3 — FGAI sobre Sentinel-3 OLCI OL_1_EFR

> **Nota:** Los productos S3 OLCI vienen en geometría de adquisición sin proyección cartográfica asignada. Las coordenadas se almacenan como tie-point grids de latitud/longitud. Es necesario convertir radiancias a R_TOA y reproyectar antes de hacer el subset.

### 3.1 Abrir el producto
- `File → Open Product` → seleccionar `xfdumanifest.xml`

### 3.2 Conversión de radiancia a reflectancia TOA
- `Optical → Preprocessing → Rad2Refl`
- Sensor: **OLCI**
- Aplicar sobre el **producto completo** (no el subset)
- Guardar resultado en disco

### 3.3 Reproyección
- `Raster → Geometric → Reprojection`
- Sistema de referencia: **WGS84 / UTM zona 30N (EPSG:32630)**
- Resolución de salida: **300 m**
- Guardar resultado en disco

### 3.4 Subset espacial y de bandas
- `Raster → Subset`
- Pestaña **Spatial Subset** → `Use Shape File...` → cargar el shapefile de embalses
- Pestaña **Band Subset** → seleccionar:

| Banda OLCI | λ (nm) | Equivalente S2 |
|------------|--------|----------------|
| Oa04 | 490 nm | B2 (azul) |
| Oa06 | 560 nm | B3 (verde) |
| Oa08 | 665 nm | B4 (rojo) |
| Oa17 | 865 nm | B8 (NIR) |

### 3.5 Calcular el FGAI
- `Raster → Band Maths`
- Nombre de la nueva banda: `FGAI_S3`
- Desmarcar **Virtual Band**
- Expresión:

```
-0.42 * Oa04_reflectance + (-0.15) * Oa06_reflectance + (-0.49) * Oa08_reflectance + 0.75 * Oa17_reflectance
```

> Comprobar los nombres exactos de las bandas en el Product Explorer tras el Rad2Refl — pueden incluir el sufijo `_reflectance`.

### 3.6 Exportar
- `File → Export → GeoTIFF`
- Exportar solo la banda `FGAI_S3`

---

## Estadísticas zonales por embalse

Para extraer estadísticas por polígono de embalse (media, máximo, percentiles) sobre los tres GeoTIFFs exportados, se recomienda usar **QGIS** o **Python con rasterstats** en lugar de SNAP, que no dispone de una herramienta de estadísticas zonales por shapefile.

### Opción A — QGIS
`Raster → Zonal Statistics`
- Capa ráster: cada uno de los tres GeoTIFFs
- Capa de polígonos: shapefile de embalses
- Estadísticas: media, mínimo, máximo, desviación típica

### Opción B — Python (rasterstats)
```python
from rasterstats import zonal_stats

stats_l1c = zonal_stats("embalses.shp", "FGAI_L1C.tif", stats=["mean", "max", "std"])
stats_l2a = zonal_stats("embalses.shp", "FAI_L2A.tif",  stats=["mean", "max", "std"])
stats_s3  = zonal_stats("embalses.shp", "FGAI_S3.tif",  stats=["mean", "max", "std"])
```

---

## Preguntas de análisis

1. ¿Introduce la falta de corrección atmosférica errores significativos en la detección de floraciones? → comparar FGAI L1C vs FAI L2A
2. ¿Los valores de FGAI son comparables entre Sentinel-2 y Sentinel-3 sobre los mismos embalses?
3. ¿A partir de qué tamaño de embalse el FGAI de Sentinel-3 es fiable? ¿Hay píxeles mixtos en los embalses más pequeños?
4. ¿Puede usarse Sentinel-3 (revisita ~2 días) como sistema de alerta temprana y Sentinel-2 (10 m) para confirmación espacial?
