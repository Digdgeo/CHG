# Día 3 — Análisis raster con Python

Última sesión del módulo de GeoPython. Trabajaremos con una imagen **Landsat 9 OLI del 27 de marzo de 2025** recortada sobre la **Reserva de la Biosfera de Doñana** — fecha con la marisma muy inundada y algo de nubosidad, ideal para practicar máscaras de calidad.

## Material

| Nº | Archivo | Contenido |
|----|---------|-----------|
| — | [`apuntes_raster.md`](./apuntes_raster.md) · [`apuntes_raster.pdf`](./apuntes_raster.pdf) | **Guía de referencia** para los alumnos: stack de librerías, conceptos clave de rasterio, tabla de índices, equivalencias Landsat/Sentinel, recetas comunes, errores típicos y GDAL CLI. |
| 03a | [`03a_intro_numpy.ipynb`](./03a_intro_numpy.ipynb) | NumPy aplicado a rasters: arrays, slicing, álgebra elemento a elemento, máscaras booleanas, estadística por eje, `np.where`. Mini-ejercicios contextualizados (NDVI, máscara de agua, clorofila). |
| 03b | [`03b_rasterio_indices_mascaras.ipynb`](./03b_rasterio_indices_mascaras.ipynb) | **GDAL bajo el capó** (gdalinfo, gdal_translate, gdalwarp) y luego Rasterio: apertura, metadatos, lectura de bandas, composiciones RGB. **Filtrado de nubes y sombras con QA_PIXEL** (decodificación bit a bit). Índices: **NDVI**, **NDWI**, **MNDWI**, **CIgreen**. Máscara de agua → poligonización. Recorte por vectorial. Estadísticas zonales. |

## Datos

El notebook **03b** trabaja con un GeoTIFF multibanda `landsat_donana_marisma.tif` que contiene **7 bandas**:

| # | Banda     | Tipo | Contenido |
|---|-----------|------|-----------|
| 1 | Blue  (B2) | float32 reflectancia | 0–1 (NaN = fuera de escena) |
| 2 | Green (B3) | float32 reflectancia | 0–1 |
| 3 | Red   (B4) | float32 reflectancia | 0–1 |
| 4 | NIR   (B5) | float32 reflectancia | 0–1 |
| 5 | SWIR1 (B6) | float32 reflectancia | 0–1 |
| 6 | SWIR2 (B7) | float32 reflectancia | 0–1 |
| 7 | QA_PIXEL   | float32 (valores enteros) | Máscara de calidad Landsat C2 bit a bit |

**Tamaño:** ~60 MB (DEFLATE, predictor=3, tiled). Recortado por `rbios.shp` (Reserva de la Biosfera de Doñana). CRS: `EPSG:32629`.

## Ejecución en Google Colab

El notebook **03b** descarga automáticamente todos los datos desde el propio repo:

- **`landsat_donana_marisma.tif`** (~60 MB) — desde un [GitHub Release](https://github.com/Digdgeo/CHG/releases/tag/dia3-landsat-donana)
- **Vectoriales `.gpkg`** — desde `raw.githubusercontent.com` (los mismos que están versionados en `dia_2/data/`)

Cero credenciales, cero URLs que rellenar — funciona en cuanto abres el notebook en Colab.

> El shape `rbios.shp` (Reserva de la Biosfera) **no se descarga**: se usó solo para preparar el recorte de la escena (script `_make_recorte.py`, apéndice del notebook). El recorte ya viene hecho.
>
> El **03a** no necesita datos externos — funciona en Colab sin más.

## Abrir directamente en Colab

Cambia `github.com` por `githubtocolab.com` en la URL del notebook:

```
https://githubtocolab.com/Digdgeo/CHG/blob/main/geopython/dia_3_analisis_raster/03a_intro_numpy.ipynb
https://githubtocolab.com/Digdgeo/CHG/blob/main/geopython/dia_3_analisis_raster/03b_rasterio_indices_mascaras.ipynb
```

## Ejecución en local

Estructura asumida:

```
geopython/
  dia_2_analisis_vectorial/data/         ← vectoriales (gpkg + rbios.shp)
  dia_3_analisis_raster/
    03a_intro_numpy.ipynb
    03b_rasterio_indices_mascaras.ipynb
    data/landsat_donana_marisma.tif      ← imagen Landsat (no versionada, ~60 MB)
```

Dependencias mínimas:

```bash
pip install numpy matplotlib rasterio rasterstats geopandas
```
