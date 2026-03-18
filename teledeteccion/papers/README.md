# Papers de referencia — Teledetección

---

## Zhang et al. (2025) — Detección automática de floraciones de cianobacterias

**Título:** Automatic detection of *Cyanobacterial* blooms using multi-source optical satellite imagery: method development and application

**Autores:** Hailong Zhang, Chen Lu, Deyong Sun, Xiaomin Ye, Shengqiang Wang, Quan Qin

**Revista:** *Ecological Indicators*, 176 (2025), 113709

**DOI:** https://doi.org/10.1016/j.ecolind.2025.113709

**Archivo:** `1-s2.0-S1470160X25006399-main.pdf`

---

### Resumen

El artículo propone el método **ACD (Automatic CyanoBloom Detection)**, un sistema automático para detectar floraciones de cianobacterias (*CyanoBloom*) en lagos a partir de imágenes ópticas multisensor.

#### Problema que resuelve
Los métodos existentes de detección de CyanoBloom requieren reflectancia de superficie corregida atmosféricamente, lo que implica datos auxiliares y preprocesamiento complejo que limita su uso operativo y su escalabilidad a múltiples sensores.

#### Solución propuesta
El método ACD trabaja directamente con la **reflectancia TOA (top-of-atmosphere)** derivada de los números digitales (DN) del satélite, evitando la corrección atmosférica. Solo necesita **4 bandas espectrales**: azul, verde, roja y NIR — disponibles en la mayoría de sensores ópticos.

#### Índice FGAI
El núcleo del método es el **Floating Green Algae Index (FGAI)**, derivado mediante una Transformación Tasseled Cap (TCT) específica para cianobacterias:

```
FGAI = -0.42 × R_TOA,blue - 0.15 × R_TOA,green - 0.49 × R_TOA,red + 0.75 × R_TOA,NIR
```

#### Flujo de trabajo (3 etapas)
1. **Procesado de imagen:** cálculo de R_TOA a partir de DN → obtención del FGAI
2. **Máscara de nubes:** diferencia entre banda roja y verde (`ΔRr-g = R_TOA,red - R_TOA,green`)
3. **Detección automática:** umbral Tc calculado automáticamente por análisis del histograma del FGAI + restricción colorimétrica CIE para eliminar falsos positivos

#### Sensores compatibles
HY1C/D-CZI · GF-WFV · GF4-PMS · HJ1-CCD · **Sentinel2-MSI** · **Landsat9-OLI** · Terra-MODIS

#### Validación
Aplicado con éxito en 6 lagos: Lake Taihu, Lake Chaohu, Lake Dianchi y Lake Xingyun (China), Lake Okeechobee (EE.UU.) y Lough Neagh (Irlanda del Norte).

---

### Relevancia para la CHG

Este método es directamente aplicable al **seguimiento de floraciones de cianobacterias en embalses del Guadalquivir** con imágenes **Sentinel-2**. Al trabajar con R_TOA sin corrección atmosférica, simplifica el flujo de trabajo operativo. Su compatibilidad con múltiples sensores permite combinar Sentinel-2 (10 m) con MODIS (500 m) para aumentar la frecuencia de revisita.
