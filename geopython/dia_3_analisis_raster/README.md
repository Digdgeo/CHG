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

El notebook **03b** detecta automáticamente si se ejecuta en Colab y descarga los datos desde Nextcloud. **Antes de la clase hay que rellenar las URL `NEXTCLOUD_…`** en la primera celda con los enlaces compartidos públicos de:

- `landsat_donana_marisma.tif` — imagen Landsat 7 bandas
- `terminos_municipales_andalucia.gpkg`
- `cuencas_guadalquivir.gpkg`
- `embalses_guadalquivir.gpkg`
- `rbios.zip` — los 4 ficheros del shapefile (`.shp`, `.shx`, `.dbf`, `.prj`) zipeados

Para que `wget` descargue directamente, el enlace de Nextcloud debe terminar en `/download`:

```
https://nextcloud.tu-dominio.es/s/TOKEN_DEL_ENLACE/download
```

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
