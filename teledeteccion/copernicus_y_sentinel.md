# El Programa Copernicus y los Satélites Sentinel

## ¿Qué es el Programa Copernicus?

**Copernicus** es el programa de observación de la Tierra de la Unión Europea, gestionado conjuntamente por la **Comisión Europea** y la **Agencia Espacial Europea (ESA)**. Es el programa de observación terrestre más ambicioso del mundo y proporciona información precisa, oportuna y de libre acceso sobre nuestro planeta y su entorno.

El programa toma su nombre del astrónomo polaco Nicolás Copérnico (1473–1543), quien revolucionó la comprensión del sistema solar al proponer el heliocentrismo.

### Objetivos principales

- Monitorizar el estado de la atmósfera, los océanos, la tierra y el cambio climático
- Apoyar la gestión de emergencias y catástrofes naturales
- Proporcionar información para la seguridad y la vigilancia fronteriza
- Dar soporte a políticas medioambientales y de desarrollo sostenible de la UE

### Datos abiertos y gratuitos

Una de las características más importantes de Copernicus es que **todos sus datos son gratuitos y de acceso libre** para cualquier usuario, ya sea ciudadano, empresa o administración pública. Los datos se descargan desde el portal oficial:

**Copernicus Data Space Ecosystem:** https://dataspace.copernicus.eu/

---

## Los Satélites Sentinel

El programa Copernicus opera su propia flota de satélites dedicados, denominados **Sentinel**. Cada familia de Sentinel está diseñada para cubrir necesidades específicas de observación, y trabajan de forma coordinada para ofrecer una cobertura global y continua.

Actualmente hay **seis familias de satélites Sentinel** operativas o en desarrollo:

---

### Sentinel-1 — Radar (SAR)

| | |
|---|---|
| **Sensor** | SAR (Radar de Apertura Sintética) en banda C |
| **Resolución** | 5–20 m |
| **Cobertura** | Global, independiente de nubes y luz solar |
| **Órbita** | ~700 km, heliosíncrona |
| **Satélites** | Sentinel-1A (2014), Sentinel-1C (2024) |

Los satélites Sentinel-1 utilizan radar de microondas, lo que les permite **observar la superficie terrestre y oceánica independientemente de las nubes o de la hora del día**. Esto los hace especialmente valiosos en situaciones de emergencia donde el cielo está cubierto.

**Aplicaciones principales:**
- Monitorización de inundaciones y deslizamientos de tierra
- Detección de vertidos de petróleo en el mar
- Seguimiento de subsidencia del terreno (interferometría SAR)
- Gestión agrícola y forestal
- Vigilancia de zonas costeras y marítimas

---

### Sentinel-2 — Óptico multiespectral de alta resolución

| | |
|---|---|
| **Sensor** | Multiespectral (13 bandas, visible + infrarrojo) |
| **Resolución** | 10, 20 y 60 m según la banda |
| **Cobertura** | Global cada 5 días (con los dos satélites) |
| **Órbita** | ~786 km, heliosíncrona |
| **Satélites** | Sentinel-2A (2015), Sentinel-2B (2017) |

Sentinel-2 es el satélite de **referencia para la teledetección óptica terrestre** dentro de Copernicus. Sus 13 bandas espectrales cubren desde el visible hasta el infrarrojo de onda corta (SWIR), permitiendo calcular una gran variedad de índices de vegetación, agua y suelo.

**Bandas principales:**

| Banda | Nombre | Longitud de onda | Resolución |
|-------|--------|-----------------|------------|
| B2 | Azul | 490 nm | 10 m |
| B3 | Verde | 560 nm | 10 m |
| B4 | Rojo | 665 nm | 10 m |
| B5 | Red Edge 1 | 705 nm | 20 m |
| B6 | Red Edge 2 | 740 nm | 20 m |
| B7 | Red Edge 3 | 783 nm | 20 m |
| B8 | NIR | 842 nm | 10 m |
| B8A | NIR estrecho | 865 nm | 20 m |
| B11 | SWIR 1 | 1610 nm | 20 m |
| B12 | SWIR 2 | 2190 nm | 20 m |

**Aplicaciones principales:**
- Monitorización de cultivos y estado de la vegetación (NDVI, EVI)
- Cartografía del uso del suelo y láminas de agua (NDWI, MNDWI)
- Detección de incendios y seguimiento de la regeneración post-incendio (NBR)
- Calidad del agua en embalses, ríos y costas
- Cartografía de nieve y hielo
- Índices de algas y floración de cianobacterias (FAI, FGAI)

---

### Sentinel-3 — Oceanografía y tierra a escala global

| | |
|---|---|
| **Sensores** | OLCI (óptico, 21 bandas), SLSTR (térmico), SRAL (altímetro radar) |
| **Resolución** | 300 m (OLCI), 500 m / 1 km (SLSTR) |
| **Cobertura** | Global cada ~2 días |
| **Órbita** | ~814 km, heliosíncrona |
| **Satélites** | Sentinel-3A (2016), Sentinel-3B (2018) |

Sentinel-3 está orientado a la **observación a escala global** de océanos y grandes masas de tierra. Su sensor principal, el **OLCI** (Ocean and Land Colour Instrument), es el sucesor del MERIS de Envisat y cubre 21 bandas espectrales a 300 m de resolución.

**Aplicaciones principales:**
- Color del océano y productividad primaria marina
- Temperatura superficial del mar y de la tierra (LST, SST)
- Monitorización de grandes embalses y masas de agua
- Detección de algas y floraciones de fitoplancton (índice FAI)
- Altimetría: nivel del mar y topografía de cuencas hidrográficas
- Variables esenciales del clima (ECV)

---

### Sentinel-4 — Composición atmosférica (geoestacionario)

| | |
|---|---|
| **Sensor** | UVN (ultravioleta, visible, infrarrojo cercano) |
| **Cobertura** | Europa y norte de África, continua |
| **Órbita** | Geoestacionaria (~36.000 km) |
| **Estado** | En desarrollo (lanzamiento previsto con Meteosat MTG-S) |

Sentinel-4 operará desde una **órbita geoestacionaria**, lo que le permitirá monitorizar continuamente la composición atmosférica sobre Europa. Al estar fijo sobre un punto de la Tierra, proporciona imágenes con alta cadencia temporal (cada hora).

**Aplicaciones principales:**
- Monitorización de contaminantes atmosféricos: NO₂, SO₂, O₃, HCHO, aerosoles
- Calidad del aire en tiempo casi real
- Soporte a políticas de reducción de emisiones

---

### Sentinel-5P — Composición atmosférica (órbita polar)

| | |
|---|---|
| **Sensor** | TROPOMI (hiperespectal UV-SWIR) |
| **Resolución** | 3,5 × 5,5 km |
| **Cobertura** | Global diaria |
| **Órbita** | ~824 km, heliosíncrona |
| **Satélites** | Sentinel-5P (2017, precursor) |

Sentinel-5P es el **precursor** de Sentinel-5 y opera en órbita polar para conseguir cobertura global diaria de la atmósfera. Su instrumento TROPOMI es el espectrómetro atmosférico de mayor resolución espacial jamás puesto en órbita.

**Aplicaciones principales:**
- Seguimiento global de NO₂ (dióxido de nitrógeno), CO, CH₄ (metano), SO₂
- Monitorización de incendios y transporte de humo
- Análisis del agujero de ozono
- Detección de emisiones industriales y volcánicas

---

### Sentinel-6 — Altimetría oceánica de referencia

| | |
|---|---|
| **Sensor** | Altímetro radar de alta resolución (Poseidón-4) |
| **Resolución** | ~300 m en modo SAR |
| **Cobertura** | Global cada 10 días |
| **Órbita** | ~1336 km |
| **Satélites** | Sentinel-6 Michael Freilich (2020) |

Sentinel-6 continúa la serie histórica de altimetría oceánica comenzada por Topex/Poseidón (1992), proporcionando mediciones de **nivel del mar con precisión centimétrica** imprescindibles para el seguimiento del cambio climático.

**Aplicaciones principales:**
- Medición del nivel medio del mar y su variación
- Corrientes oceánicas y circulación termohalina
- Batimetría de zonas costeras
- Vigilancia de inundaciones costeras

---

## Resumen comparativo

| Satélite | Sensor | Resolución espacial | Revisita | Dominio principal |
|----------|--------|-------------------|----------|------------------|
| Sentinel-1 | SAR (banda C) | 5–20 m | 6 días (1 sat) | Tierra, Océano (todo tiempo) |
| Sentinel-2 | Multiespectral óptico | 10–60 m | 5 días (2 sat) | Tierra |
| Sentinel-3 | OLCI, SLSTR, SRAL | 300 m – 1 km | ~2 días | Océano, Tierra global |
| Sentinel-4 | UVN (geoest.) | ~8 km | Continua (1h) | Atmósfera (Europa) |
| Sentinel-5P | TROPOMI | 3,5 × 5,5 km | Diaria | Atmósfera (global) |
| Sentinel-6 | Altímetro radar | ~300 m | 10 días | Nivel del mar |

---

## Copernicus en la gestión hídrica

Para organismos como la **Confederación Hidrográfica del Guadalquivir**, los satélites Copernicus/Sentinel ofrecen capacidades de gran valor:

- **Sentinel-1:** detección y cartografía de inundaciones en tiempo casi real, incluso con cielo cubierto
- **Sentinel-2:** monitorización de embalses (lámina de agua, turbidez, vegetación riparia), cartografía de regadíos, detección de sequías
- **Sentinel-3:** seguimiento de grandes embalses, calidad del agua (índice FAI/FGAI para algas), temperatura superficial
- **Sentinel-5P:** calidad del aire en la cuenca, detección de quemas de rastrojos

---

## Recursos y portales oficiales

| Recurso | URL |
|---------|-----|
| Portal de datos Copernicus | https://dataspace.copernicus.eu/ |
| Web oficial Copernicus (CE) | https://www.copernicus.eu/ |
| Misiones Sentinel (ESA) | https://sentinel.esa.int/ |
| Servicios Copernicus | https://www.copernicus.eu/en/copernicus-services |
| SNAP (software de procesado) | https://step.esa.int/ |
