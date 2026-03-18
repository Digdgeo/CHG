# 🛰️ Guía de Referencia: Productos Sentinel-3
> Fuente: ESA Sentinel Online / Copernicus Data Space Ecosystem  
> Última revisión: marzo 2026

---

## Índice
1. [Cómo leer un nombre de producto](#1-cómo-leer-un-nombre-de-producto)
2. [Niveles de procesado](#2-niveles-de-procesado)
3. [OLCI — Instrumento óptico (color)](#3-olci--ocean-and-land-colour-instrument)
4. [SLSTR — Radiómetro térmico](#4-slstr--sea-and-land-surface-temperature-radiometer)
5. [SYNERGY — Fusión OLCI + SLSTR](#5-synergy--fusión-olci--slstr)
6. [SRAL/MWR — Altímetro radar](#6-sralmwr--sar-radar-altimeter)
7. [Radiancias vs Reflectancias](#7-radiancias-vs-reflectancias-qué-descargar-para-cada-uso)
8. [Productos útiles para calidad de aguas](#8-productos-útiles-para-calidad-de-aguas)
9. [Timeliness: NRT vs STC vs NTC](#9-timeliness-nrt-vs-stc-vs-ntc)
10. [Filtros en el Copernicus Data Space Browser](#10-filtros-en-el-copernicus-data-space-browser)

---

## 1. Cómo leer un nombre de producto

```
S3A_OL_2_WFR____20250615T110838_20250615T111138_20250616T183942_0179_127_094_2340_MAR_O_NT_003.SEN3
 │   │  │  │         │                │                │          │    │   │   │    │   │  │   │
 │   │  │  │         │                │                │          │    │   │   │    │   │  │   └── Baseline procesado
 │   │  │  │         │                │                │          │    │   │   │    │   │  └────── Timeliness (NR/ST/NT)
 │   │  │  │         │                │                │          │    │   │   │    │   └───────── Origen (O=operacional)
 │   │  │  │         │                │                │          │    │   │   │    └───────────── Centro procesado
 │   │  │  │         │                │                │          │    │   │   └────────────────── Ciclo de órbita relativa
 │   │  │  │         │                │                │          │    │   └────────────────────── Nº órbita relativa
 │   │  │  │         │                │                │          │    └────────────────────────── Ciclo absoluto
 │   │  │  │         │                │                │          └─────────────────────────────── Duración (segundos)
 │   │  │  │         │                │                └────────────────────────────────────────── Tiempo generación
 │   │  │  │         │                └─────────────────────────────────────────────────────────── Fin sensing
 │   │  │  │         └──────────────────────────────────────────────────────────────────────────── Inicio sensing
 │   │  │  └────────────────────────────────────────────────────────────────────────────────────── Tipo producto
 │   │  └───────────────────────────────────────────────────────────────────────────────────────── Nivel (1=L1, 2=L2)
 │   └──────────────────────────────────────────────────────────────────────────────────────────── Instrumento (OL/SL/SR/SY)
 └──────────────────────────────────────────────────────────────────────────────────────────────── Satélite (S3A / S3B)
```

---

## 2. Niveles de procesado

| Nivel | Descripción | Estado del dato |
|-------|-------------|----------------|
| **L0** | Datos brutos del sensor (telemetría) | No disponible para usuarios |
| **L1B** | Calibrado radiométricamente y geolocalizados | Radiancias o temperaturas de brillo |
| **L1C** | Solo en SYNERGY: registro conjunto OLCI+SLSTR | Radiancias/reflectancias TOA fusionadas |
| **L2** | Parámetros geofísicos derivados | Reflectancias, clorofila, TSM, LST, SST... |

---

## 3. OLCI — Ocean and Land Colour Instrument

**Instrumento:** Espectrómetro push-broom con 5 cámaras  
**Bandas:** 21 (400–1020 nm)  
**Resolución:** 300 m (FR) / 1.2 km (RR)  
**Revisita:** ~2 días (con S3A+S3B combinados)  
**Cobertura:** Global  
**Herencia:** MERIS (Envisat)  

### 3.1 Tabla completa de productos OLCI

| Código | Nombre completo | Nivel | Resolución | Unidad principal | Contenido clave | Aplicación |
|--------|----------------|-------|------------|-----------------|-----------------|------------|
| `OL_1_EFR` | EO Full Resolution | L1B | 300 m | **Radiancia TOA** (W/m²/sr/μm) | 21 bandas de radiancia + flags | Base para procesos propios; visualización RGB |
| `OL_1_ERR` | EO Reduced Resolution | L1B | 1.2 km | **Radiancia TOA** | 21 bandas de radiancia + flags | Vista rápida; cobertura global |
| `OL_2_WFR` | Water Full Resolution | L2 | 300 m | **Reflectancia marina** (Rrs, sr⁻¹) | CHL_OC4ME, CHL_NN, TSM_NN, CDOM, aerosoles, Kd490 | ⭐ **Calidad de agua — PRODUCTO PRINCIPAL** |
| `OL_2_WRR` | Water Reduced Resolution | L2 | 1.2 km | **Reflectancia marina** (Rrs) | Igual que WFR pero a menor resolución | Series temporales largas; escala regional |
| `OL_2_LFR` | Land Full Resolution | L2 | 300 m | **Reflectancia terrestre** (TOC-R) | OGVI, OTCI, RC681, RC865, FAPAR, IWV | Vegetación; cubiertas terrestres; cuenca terrestre |
| `OL_2_LRR` | Land Reduced Resolution | L2 | 1.2 km | **Reflectancia terrestre** (TOC-R) | Igual que LFR pero a menor resolución | Escala global/regional; series temporales |

### 3.2 Variables clave del OL_2_WFR (calidad de agua)

| Variable | Descripción | Unidad | Rango típico |
|----------|-------------|--------|-------------|
| `CHL_OC4ME` | Clorofila-a (algoritmo OC4ME, herencia MERIS) | mg/m³ | 0.01–100 |
| `CHL_NN` | Clorofila-a (red neuronal) | mg/m³ | 0.01–100 |
| `TSM_NN` | Sólidos en suspensión totales (red neuronal) | g/m³ | 0.01–100 |
| `CDM_NN` | CDOM + detritus (materia orgánica coloreada disuelta) | m⁻¹ | 0.001–10 |
| `IWV` | Vapor de agua integrado | kg/m² | — |
| `Kd490` | Coeficiente de atenuación difusa a 490 nm | m⁻¹ | 0.01–10 |
| `Oa*_reflectance` | Reflectancias de agua corregidas por atmósfera (21 bandas) | sr⁻¹ | 0–0.1 |
| `WQSF` | Flags de calidad del agua (INVALID, CLOUD, CLOUD_SHADOW...) | Bitmask | — |

### 3.3 Variables clave del OL_2_LFR (tierra)

| Variable | Descripción | Unidad |
|----------|-------------|--------|
| `OGVI` | OLCI Global Vegetation Index (≈ FAPAR) | adimensional (0–1) |
| `OTCI` | OLCI Terrestrial Chlorophyll Index | adimensional |
| `RC681` | Reflectancia corregida Rayleigh a 681 nm (rojo) | adimensional |
| `RC865` | Reflectancia corregida Rayleigh a 865 nm (NIR) | adimensional |
| `FAPAR` | Fracción de radiación fotosintéticamente activa absorbida | adimensional (0–1) |

> 💡 **RC681 y RC865** permiten calcular NDVI directamente:  
> `NDVI = (RC865 - RC681) / (RC865 + RC681)`

---

## 4. SLSTR — Sea and Land Surface Temperature Radiometer

**Instrumento:** Radiómetro de doble vista (nadir + oblicua)  
**Bandas:** 9 espectrales + 2 de fuego  
**Resolución:** 500 m (VNIR/SWIR, bandas S1–S6) / 1 km (TIR, bandas S7–S9 + F1–F2)  
**Cobertura:** Global, swath ~1400 km  
**Herencia:** AATSR (Envisat)  

### 4.1 Bandas espectrales SLSTR

| Banda | λ central (μm) | Resolución | Región espectral | Uso principal |
|-------|---------------|------------|-----------------|---------------|
| S1 | 0.555 | 500 m | Verde (VIS) | Detección nubosa |
| S2 | 0.659 | 500 m | Rojo (VIS) | Detección nubosa |
| S3 | 0.865 | 500 m | NIR | Vegetación; nubosidad |
| S4 | 1.375 | 500 m | SWIR | Cirros |
| S5 | 1.610 | 500 m | SWIR | Vegetación; corrección atmósferas turbias |
| S6 | 2.250 | 500 m | SWIR | Minerales; corrección aguas turbias |
| S7 | 3.740 | 1 km | MWIR | Fuegos; SST (noche) |
| S8 | 10.85 | 1 km | TIR | **LST / SST principal** |
| S9 | 12.00 | 1 km | TIR | **LST / SST (corrección split-window)** |
| F1 | 3.740 | 1 km | MWIR | Detección fuegos activos |
| F2 | 10.85 | 1 km | TIR | Detección fuegos activos |

### 4.2 Tabla completa de productos SLSTR

| Código | Nombre completo | Nivel | Resolución | Unidad principal | Contenido clave | Aplicación |
|--------|----------------|-------|------------|-----------------|-----------------|------------|
| `SL_1_RBT` | Radiances and Brightness Temperatures | L1B | 500 m / 1 km | **Radiancia** (mW/m²/sr/cm⁻¹) + **Temperatura de brillo** (K) | Todas las bandas, vista nadir y oblicua | Base para procesos propios LST/SST |
| `SL_2_LST` | Land Surface Temperature | L2 | 1 km | **Temperatura** (K) | LST, incertidumbre, clasificación biomas, máscara nubes | ⭐ Temperatura superficial terrestre (embalses, riberas) |
| `SL_2_WST` | Water Surface Temperature | L2 | ~1 km | **Temperatura** (K) | SST, incertidumbre, flags | Temperatura superficial del mar / estuarios |
| `SL_2_FRP` | Fire Radiative Power | L2 | 1 km | Potencia radiativa (MW) | Localización y FRP de incendios activos | Detección y seguimiento de incendios |

### 4.3 Variables clave del SL_2_LST

| Variable | Descripción | Unidad |
|----------|-------------|--------|
| `LST` | Temperatura superficial terrestre | K (Kelvin) |
| `LST_uncertainty` | Incertidumbre de la LST | K |
| `biome` | Clasificación del bioma del píxel | Categórica |
| `bayes_in` | Flag de máscara de nubes Bayesiana | Bitmask |
| `confidence_in` | Flags de confianza (day, twilight, cloud...) | Bitmask |

> ⚠️ **Atención:** LST a 1 km tiene limitaciones sobre embalses pequeños (<5 km de anchura). Agua y tierra se mezclan en píxeles mixtos.

---

## 5. SYNERGY — Fusión OLCI + SLSTR

**Base:** Fusión de `OL_1_EFR` + `SL_1_RBT`  
**Cobertura:** **Solo tierra** (píxeles de agua interior excluidos por máscara)  
**Resolución:** 300 m (resolución OLCI)  
**Revisita:** <2 días  

> ⚠️ **IMPORTANTE:** Los embalses y ríos quedan enmascarados como agua interior y aparecen como NO DATA en los productos SYN L2 de tierra. Para calidad de aguas usar `OL_2_WFR`.

### 5.1 Tabla completa de productos SYNERGY

| Código | Nombre completo | Nivel | Resolución | Unidad principal | Contenido clave | Aplicación |
|--------|----------------|-------|------------|-----------------|-----------------|------------|
| `SY_1_MISR` | Multi-Instrument Super-Resolution | L1C | 300 m | Radiancia / Reflectancia TOA | Grids de correspondencia OLCI+SLSTR en geometría de adquisición | No distribuido a usuarios finales |
| `SY_2_SYN` | Surface Reflectance and Aerosol | L2 | 300 m | **Reflectancia superficial** (SDR) | 26 bandas corregidas atm. (16 OLCI + 10 SLSTR nadir/oblicua), AOT, Ångström | ⭐ Mejor producto de reflectancia corregida sobre tierra |
| `SY_2_VGP` | VEGETATION-like TOA P | L2 | 300 m | **Reflectancia TOA** | 4 bandas estilo SPOT-VGT (B0, B2, B3, MIR) | Continuidad con SPOT-VEGETATION |
| `SY_2_VG1` | VEGETATION-like S1 (diario) | L2 | 1 km | **Reflectancia superficial** + NDVI | Composición diaria VEGETATION | Series temporales de vegetación |
| `SY_2_V10` | VEGETATION-like S10 (decenal) | L2 | 1 km | **Reflectancia superficial** + NDVI | Composición decenal (10 días) VEGETATION | Monitoreo agrícola; escala regional |
| `SY_2_AOD` | Aerosol Optical Depth | L2 | 4.5 km | Espesor óptico (adim.) | AOT@550 nm, modelo de aerosol, Ångström; tierra **y** mar | Calidad del aire; corrección atmosférica |

### 5.2 Bandas del SY_2_SYN

| ID banda | Instrumento | λ (nm) | Vista |
|----------|-------------|--------|-------|
| Oa01–Oa12, Oa16–Oa21 | OLCI | 400–1020 | Nadir |
| S1_n, S2_n, S3_n, S5_n, S6_n | SLSTR | 555–2250 | Nadir |
| S1_o, S2_o, S3_o, S5_o, S6_o | SLSTR | 555–2250 | Oblicua |

---

## 6. SRAL/MWR — SAR Radar Altimeter

**Instrumento:** Altímetro SAR en banda Ku + radiómetro de microondas  
**Resolución espacial:** ~300 m a lo largo del track / ~1–2 km transversal  
**Herramienta recomendada:** Sentinel Altimetry Toolbox (no SNAP óptico)  
**Nota:** Perfecto para monitorizar nivel de agua en embalses y ríos  

| Código | Nombre | Nivel | Contenido | Aplicación |
|--------|--------|-------|-----------|------------|
| `SR_1_SRA` | L1 SAR | L1B | Ecos SAR calibrados, apilados | Procesado avanzado |
| `SR_1_SRA_A` | L1 SAR (versión A) | L1B | Ecos SAR (versión alternativa) | Procesado avanzado |
| `SR_1_SRA_BS` | L1 SAR BS | L1B | Espectro de haz | Procesado avanzado |
| `SR_2_LAN` | Land Altimetry | L2 | Elevación superficial sobre tierra, ríos, lagos | ⭐ Nivel de agua en embalses y ríos |
| `SR_2_LAN_HY` | Hydrology Thematic | L2 | Elevación optimizada para hidrología (retrackers SAR) | ⭐ Nivel de embalses (producto recomendado desde 2023) |
| `SR_2_LAN_SI` | Sea Ice Thematic | L2 | Freeboards de hielo marino | Ártico/Antártico |
| `SR_2_LAN_LI` | Land Ice Thematic | L2 | Topografía de capas de hielo | Groenlandia/Antártico |
| `SR_2_WAT` | Ocean Altimetry | L2 | Altura del nivel del mar, velocidad del viento | Oceanografía |

---

## 7. Radiancias vs Reflectancias: ¿qué descargar para cada uso?

| Necesidad | Producto | Unidad | ¿Listo para usar? |
|-----------|----------|--------|-------------------|
| Ver colores / RGB | `OL_1_EFR` | Radiancia (W/m²/sr/μm) | Requiere factor escala |
| Clorofila, turbidez, CDOM | `OL_2_WFR` | Reflectancia Rrs (sr⁻¹) | ✅ Sí — ya corregido atmosféricamente |
| Índices vegetación (NDVI) sobre tierra | `OL_2_LFR` | Reflectancia TOC (adim.) | ✅ Sí — corrección Rayleigh aplicada |
| Reflectancia superficial completa tierra | `SY_2_SYN` | Reflectancia SDR (adim.) | ✅ Sí — corrección atmosférica completa |
| Temperatura superficial terrestre | `SL_2_LST` | Kelvin (K) | ✅ Sí |
| Temperatura superficial marina | `SL_2_WST` | Kelvin (K) | ✅ Sí |
| Nivel de agua en embalse | `SR_2_LAN_HY` | Metros (m, ellipsoide WGS84) | ✅ Sí |
| Procesar tu propio algoritmo desde L1 | `OL_1_EFR` o `SL_1_RBT` | Radiancia / T. brillo | ❌ Requiere corrección atmosférica |

---

## 8. Productos útiles para calidad de aguas

### Caso de estudio: cuenca del Guadalquivir

| Objetivo | Producto | Variable | Resolución | Limitación |
|----------|----------|----------|------------|------------|
| Clorofila-a | `OL_2_WFR` | `CHL_OC4ME` o `CHL_NN` | 300 m | Embalses <3 km: pocos píxeles válidos |
| Turbidez / sedimentos | `OL_2_WFR` | `TSM_NN` | 300 m | Idem |
| Materia orgánica disuelta | `OL_2_WFR` | `CDM_NN` | 300 m | Idem |
| Temperatura superficial | `SL_2_LST` | `LST` | 1 km | Píxeles mixtos en ríos estrechos |
| Temperatura estuario/mar | `SL_2_WST` | `WST` | ~1 km | Solo zona marina/costera |
| Vegetación ribereña / cuenca | `OL_2_LFR` | `OGVI`, `RC681`, `RC865` | 300 m | Embalses excluidos (son agua) |
| Nivel del embalse | `SR_2_LAN_HY` | `elevation_ocog_20_ku` | ~300 m track | Solo donde pasa el track (cada 27 días) |
| Índices espectrales avanzados | `SY_2_SYN` | 26 bandas SDR | 300 m | **No cubre píxeles de agua** |

### Viabilidad por embalse (resolución OLCI 300 m)

| Embalse | Superficie (km²) | Píxeles OLCI ~válidos | Viabilidad |
|---------|-----------------|----------------------|------------|
| Iznájar (Córdoba) | 38 km² | ~400 | ✅ Buena |
| La Serena (Badajoz) | 112 km² | ~1240 | ✅ Excelente |
| Alcalá del Río | ~10 km² | ~110 | ⚠️ Limitada (¿>50%?) |
| La Minilla (Sevilla) | ~5 km² | ~55 | ❌ Muy limitada |
| Estuario Guadalquivir | >100 km² | Amplio | ✅ Excelente |

---

## 9. Timeliness: NRT vs STC vs NTC

| Código | Nombre | Disponibilidad | Calidad | Cuándo usarlo |
|--------|--------|---------------|---------|---------------|
| `NR` | Near Real Time | < 3 horas | ⭐⭐ (calibración preliminar) | Operativo, alertas, monitoreo en tiempo casi-real |
| `ST` | Short Time Critical | < 48 horas | ⭐⭐⭐ | Aplicaciones que necesitan rapidez y buena calidad |
| `NT` | Non-Time Critical | 1–3 semanas | ⭐⭐⭐⭐⭐ (calibración final) | ✅ **Investigación y docencia** — usar siempre que sea posible |

> 💡 Para un curso/ejercicio práctico, usa siempre **NT** (Not Time Critical). Los productos del listado que has pegado tienen `NT_003` o `NT_004` al final del nombre — son los de máxima calidad.

---

## 10. Filtros en el Copernicus Data Space Browser

### ⚠️ Nota sobre filtro de nubes en Sentinel-3
A diferencia de Sentinel-2, **Sentinel-3 no tiene un filtro de cobertura nubosa disponible directamente en el browser** para productos OLCI L2. La razón es que la máscara de nubes se genera dentro del producto (flags `WQSF` para agua, flags de confianza para SLSTR).

**Alternativas prácticas:**
1. **Usa el preview visual** del producto en el browser — activa la vista RGB antes de descargar
2. **Criterio estacional:** junio–septiembre en el Guadalquivir = baja nubosidad. Mayo–septiembre es la época más favorable
3. **Descarga y verifica rápido en SNAP:** abre el `OL_1_EFR` (es liviano el preview), visualiza RGB y comprueba nubes antes de trabajar con el WFR
4. **Usa la API OData** si quieres automatizar la búsqueda por porcentaje nuboso en productos que sí lo incluyen

### Filtros recomendados en el browser para Sentinel-3

```
Mission:        SENTINEL-3
Instrument:     OLCI  (o SLSTR, según lo que busques)
Product type:   OL_2_WFR  (escribe solo el tipo, sin guiones bajos al final)
Date range:     mayo–septiembre (menos nubes sobre Andalucía)
Timeliness:     NT (Non-Time Critical)
Área:           Dibuja polígono sobre cuenca del Guadalquivir
```

### Lista de tipos de producto para copiar en el buscador

| Lo que quieres | Escribe en "Product type" |
|----------------|--------------------------|
| Clorofila + turbidez | `OL_2_WFR` |
| Vegetación terrestre | `OL_2_LFR` |
| Temperatura terrestre | `SL_2_LST` |
| Temperatura marina | `SL_2_WST` |
| Reflectancia corregida tierra | `SY_2_SYN` |
| Nivel de agua embalses | `SR_2_LAN_HY` |
| RGB base (L1B) | `OL_1_EFR` |

---

## Apéndice: Resumen visual por instrumento

```
SENTINEL-3
├── OLCI (óptico, 21 bandas, 300 m)
│   ├── L1B → OL_1_EFR (FR) / OL_1_ERR (RR)  →  RADIANCIAS TOA
│   └── L2  → OL_2_WFR (FR) / OL_2_WRR (RR)  →  REFLECTANCIAS agua (Rrs)
│           → OL_2_LFR (FR) / OL_2_LRR (RR)  →  REFLECTANCIAS tierra (TOC-R)
│
├── SLSTR (térmico + óptico, 500 m / 1 km)
│   ├── L1B → SL_1_RBT            →  RADIANCIAS + TEMPERATURAS DE BRILLO
│   └── L2  → SL_2_LST            →  TEMPERATURA terrestre (K)
│           → SL_2_WST            →  TEMPERATURA marina (K)
│           → SL_2_FRP            →  POTENCIA RADIATIVA fuegos (MW)
│
├── SYNERGY (fusión OLCI+SLSTR, solo tierra, 300 m)
│   ├── L1C → SY_1_MISR           →  No distribuido
│   └── L2  → SY_2_SYN            →  REFLECTANCIAS superficiales (26 bandas)
│           → SY_2_VGP/VG1/V10    →  REFLECTANCIAS + NDVI estilo VEGETATION
│           → SY_2_AOD            →  ESPESOR ÓPTICO aerosoles (tierra+mar)
│
└── SRAL/MWR (altímetro radar, track ~300 m)
    ├── L1B → SR_1_SRA / SR_1_SRA_A / SR_1_SRA_BS  →  Ecos SAR crudos
    └── L2  → SR_2_LAN_HY         →  NIVEL AGUA (hidrología, embalses)
            → SR_2_LAN_SI         →  HIELO MARINO
            → SR_2_LAN_LI         →  HIELO TERRESTRE
            → SR_2_WAT            →  NIVEL DEL MAR (oceanografía)
```

---

*Documento generado como referencia de trabajo para curso de teledetección aplicada a calidad de aguas — Guadalquivir.*
