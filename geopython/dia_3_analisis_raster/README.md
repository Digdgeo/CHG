# Día 3 — Análisis raster con Python

Última sesión del módulo de GeoPython. Trabajaremos con una imagen Landsat 8/9 recortada sobre **Doñana y el bajo Guadalquivir**.

## Material

| Nº | Archivo | Contenido |
|----|---------|-----------|
| — | [`apuntes_raster.md`](./apuntes_raster.md) | **Guía de referencia** para los alumnos: stack de librerías, conceptos clave de rasterio, tabla de índices, equivalencias Landsat/Sentinel, recetas comunes, errores típicos y GDAL CLI. |
| 03a | [`03a_intro_numpy.ipynb`](./03a_intro_numpy.ipynb) | NumPy aplicado a rasters: arrays, slicing, álgebra elemento a elemento, máscaras booleanas, estadística por eje, `np.where`. Mini-ejercicios contextualizados (NDVI, máscara de agua, clorofila). |
| 03b | [`03b_rasterio_indices_mascaras.ipynb`](./03b_rasterio_indices_mascaras.ipynb) | **GDAL bajo el capó** (gdalinfo, gdal_translate, gdalwarp) y luego Rasterio: apertura, metadatos, lectura de bandas, composiciones RGB. Índices: **NDVI**, **NDWI**, **MNDWI**, **CIgreen**. Máscara de agua → poligonización. Recorte por vectorial. Estadísticas zonales. |

## Ejecución en Google Colab

El notebook **03b** detecta automáticamente si se ejecuta en Colab y descarga los datos desde Nextcloud. **Antes de la clase hay que rellenar las URL `NEXTCLOUD_…`** en la primera celda con los enlaces compartidos públicos de:

- `landsat_donana.tif` — imagen Landsat 6 bandas (Blue, Green, Red, NIR, SWIR1, SWIR2), float32, ya reescalada a reflectancia 0–1
- `terminos_municipales_andalucia.gpkg`
- `cuencas_guadalquivir.gpkg`
- `embalses_guadalquivir.gpkg`

Para que `wget` descargue directamente, el enlace de Nextcloud debe terminar en `/download`:

```
https://nextcloud.tu-dominio.es/s/TOKEN_DEL_ENLACE/download
```

> El **03a** no necesita datos externos — funciona en Colab sin más.

## Ejecución en local

Estructura asumida:

```
geopython/
  dia_2_analisis_vectorial/data/         ← vectoriales (gpkg)
  dia_3_analisis_raster/
    03a_intro_numpy.ipynb
    03b_rasterio_indices_mascaras.ipynb
    data/landsat_donana.tif              ← imagen Landsat (no versionada)
```

Dependencias mínimas:

```bash
pip install numpy matplotlib rasterio rasterstats geopandas
```
