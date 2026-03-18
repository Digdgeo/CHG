# GeoPython

Módulo de Python aplicado a los Sistemas de Información Geográfica.

## Clase 1 — Introducción y datos vectoriales

### Contenidos
- Entorno de trabajo: Python, Jupyter y librerías geoespaciales
- Introducción a `geopandas`: lectura, escritura y exploración de datos vectoriales
- Sistemas de referencia de coordenadas con `pyproj`
- Operaciones espaciales: reproyección, selección, dissolve, buffer
- Visualización básica con `matplotlib`

---

## Clase 2 — Datos raster

### Contenidos
- Introducción a `rasterio`: lectura y escritura de rasters
- Inspección de metadatos y transformaciones
- Operaciones con rasters: recorte, remuestreo, álgebra de bandas
- Integración vector-raster: enmascaramiento y estadísticas zonales con `rasterstats`

---

## Clase 3 — Análisis y visualización avanzada

### Contenidos
- Visualización interactiva con `folium` y `leafmap`
- Análisis espacial avanzado con `geopandas` y `shapely`
- Flujo de trabajo completo: caso práctico aplicado a la cuenca del Guadalquivir
- Exportación de resultados y generación de mapas

---

## Requisitos

Instalar el entorno con conda o mamba:

```bash
conda create -n geopython python=3.11
conda activate geopython
conda install -c conda-forge geopandas rasterio rasterstats matplotlib folium leafmap jupyter
```

### Datos de prácticas
Los datos utilizados en las prácticas se encuentran en las carpetas `clase1/datos/`, `clase2/datos/` y `clase3/datos/`.
