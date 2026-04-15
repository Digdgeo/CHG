# GeoPython

Módulo de Python aplicado a los Sistemas de Información Geográfica.

## Día 1 — Introducción a Python

### Contenidos
- Entorno de trabajo: Python, Jupyter y librerías geoespaciales
- Introducción a Python: tipos de datos, estructuras de control, funciones
- Clases y programación orientada a objetos
- Manejo de datos tabulares con `pandas`

---

## Día 2 — Datos vectoriales y nubes de puntos

### Contenidos
- Introducción a `geopandas`: lectura, escritura y exploración de datos vectoriales
- Sistemas de referencia de coordenadas con `pyproj`
- Operaciones espaciales: reproyección, selección, dissolve, buffer
- Nubes de puntos LiDAR con `laspy` y `open3d`

---

## Día 3 — Datos raster

### Contenidos
- Introducción a `rasterio`: lectura y escritura de rasters
- Inspección de metadatos y transformaciones
- Operaciones con rasters: recorte, remuestreo, álgebra de bandas
- Integración vector-raster: enmascaramiento y estadísticas zonales con `rasterstats`

---

## Día 4 — Análisis de imágenes Landsat

### Contenidos
- Acceso y descarga de imágenes Landsat
- Cálculo de índices espectrales (NDVI, NDWI, etc.)
- Análisis multitemporal con series de imágenes Landsat
- Visualización y exportación de resultados

---

## Requisitos

Instalar el entorno con conda o mamba:

```bash
conda create -n geopython python=3.11
conda activate geopython
conda install -c conda-forge geopandas rasterio rasterstats matplotlib folium leafmap jupyter
```

### Datos de prácticas
Los datos utilizados en las prácticas se encuentran en las carpetas correspondientes a cada día.
