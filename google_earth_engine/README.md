# Google Earth Engine

Módulo de análisis geoespacial a gran escala con la plataforma Google Earth Engine (GEE).

## Requisitos previos
- Cuenta de Google Earth Engine: https://earthengine.google.com/
- Registro del proyecto en Google Cloud Console

---

## Clase 1 — Introducción a GEE

### Contenidos
- ¿Qué es Google Earth Engine? Arquitectura y capacidades
- El Code Editor: interfaz, JavaScript API
- Colecciones de imágenes: `ImageCollection` e `Image`
- Filtrado por fecha, región y metadatos
- Visualización de imágenes en el mapa
- Índices espectrales: NDVI, NDWI, NBR
- Exportación de resultados a Google Drive

---

## Clase 2 — Análisis de series temporales

### Contenidos
- Construcción de series temporales con GEE
- Reducción de colecciones: mediana, máximo, percentiles
- Composición de imágenes sin nubes
- Detección de cambios: comparación multitemporal
- Gráficos de series temporales con la API de Python (`geemap`)

---

## Clase 3 — Aplicaciones avanzadas y API Python

### Contenidos
- Introducción a `geemap`: GEE desde Python/Jupyter
- Clasificación supervisada de usos del suelo
- Análisis hidrológico: cuencas, índices de humedad
- Caso práctico: monitorización de masas de agua en la cuenca del Guadalquivir
- Exportación y postprocesado de resultados

---

## Recursos

- **GEE Code Editor**: https://code.earthengine.google.com/
- **geemap**: https://geemap.org/
- **Catálogo de datos GEE**: https://developers.google.com/earth-engine/datasets
- **Documentación oficial**: https://developers.google.com/earth-engine/

---

### Datos de prácticas
Los scripts y notebooks de cada clase se encuentran en `clase1/`, `clase2/` y `clase3/`.
