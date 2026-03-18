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

---

## Índice de referencia: FAI original (Hu, 2009)

El FGAI de Zhang et al. (2025) es una evolución del **FAI (Floating Algae Index)** propuesto originalmente por Hu (2009), que es el índice de referencia citado en el paper y que sí requiere imágenes con corrección atmosférica.

**Referencia:** Hu, C. (2009). A novel ocean color index to detect floating algae in the global oceans. *Remote Sensing of Environment*, 113(10), 2118–2129.
**DOI:** https://doi.org/10.1016/j.rse.2009.05.012

### Fórmula

El FAI se calcula como la diferencia entre la reflectancia en el NIR y una línea base interpolada entre la banda roja y la banda SWIR:

```
FAI = R_rc(NIR) - R_rc'(NIR)

donde:
R_rc'(NIR) = R_rc(red) + [R_rc(SWIR) - R_rc(red)] × (λ_NIR - λ_red) / (λ_SWIR - λ_red)
```

`R_rc` = reflectancia corregida de Rayleigh (corrección atmosférica parcial)

### Bandas por sensor

| Sensor | Banda roja | Banda NIR | Banda SWIR |
|--------|-----------|-----------|------------|
| Sentinel-2 MSI | B4 (~665 nm) | B8A (~865 nm) | B11 (~1610 nm) |
| Sentinel-3 OLCI | Oa10 (~681 nm) | Oa17 (~865 nm) | — (sin SWIR) |
| Landsat 8/9 OLI | B4 (~655 nm) | B5 (~865 nm) | B6 (~1609 nm) |

> **Nota:** Sentinel-3 OLCI no dispone de banda SWIR, por lo que el FAI original no es directamente aplicable. Para S3 se recomienda usar los productos `OL_2_WFR` con las variables `CHL_OC4ME` o `CHL_NN`.

### FAI vs FGAI

| | FAI (Hu, 2009) | FGAI (Zhang et al., 2025) |
|-|---------------|--------------------------|
| Corrección atmosférica | Sí (Rayleigh) | No (trabaja con R_TOA) |
| Bandas necesarias | Roja + NIR + SWIR | Azul + Verde + Roja + NIR |
| Umbral | Manual | Automático (histograma) |
| Sensores compatibles | Los que tengan SWIR | Mayoría de sensores ópticos |

---

## Apunte teórico: ¿cómo aplicar la corrección Rayleigh a Sentinel-2?

Aunque para el ejercicio usaremos directamente los productos L1C y L2A, la corrección Rayleigh puede aplicarse como paso intermedio por tres vías:

### 1. Con SNAP (interfaz gráfica)
SNAP incluye el operador **Rayleigh Correction Processor**:
- `Optical → Preprocessing → Rayleigh Correction`
- Funciona directamente sobre el producto L1C
- Genera bandas `rBRR` (Rayleigh-corrected Bottom of Rayleigh Reflectance) listas para calcular el FAI

### 2. Con `esa_snappy` (Python)
Llamando al mismo operador de SNAP desde Python:
```python
import esa_snappy
from esa_snappy import ProductIO, GPF, HashMap

product = ProductIO.readProduct("S2A_L1C.SAFE")
params = HashMap()
params.put('computeTaur', True)
params.put('addAirMass', False)
rc_product = GPF.createProduct('RayleighCorrection', params, product)
```

### 3. Con `py6s` (modelo de transferencia radiativa)
`py6s` es un wrapper de Python para el modelo **6S** — permite calcular la corrección Rayleigh (y de aerosoles) de forma más rigurosa:
```bash
pip install Py6S
```

> **Nota:** Para nuestro contexto, la corrección Rayleigh como paso intermedio tiene poco sentido cuando el producto L2A ya está disponible gratuitamente en el Copernicus Data Space. Su interés es más histórico: el FAI original (Hu, 2009) fue diseñado para sensores oceanográficos (MODIS, SeaWiFS) donde los productos de reflectancia de superficie no siempre eran fiables en zonas costeras e interiores.

---

## Propuesta de ejercicio: comparación de índices en embalses del Guadalquivir

### Objetivo
Evaluar el efecto del nivel de corrección atmosférica y la resolución espacial en la detección de floraciones, calculando los índices FAI/FGAI sobre tres fuentes de datos distintas y comparando los resultados.

### Embalses candidatos

| Embalse | Provincia |
|---------|-----------|
| Bornos | Cádiz |
| Guadalcacín | Cádiz |
| Torre del Águila | Sevilla |

### Diseño del ejercicio

Los tres escenarios se calculan sobre la misma fecha (o la más próxima disponible):

| Escenario | Producto | Índice | Resolución | Corrección atmosférica |
|-----------|----------|--------|------------|----------------------|
| 1 | Sentinel-2 **L2A** | **FAI** (roja + NIR + SWIR) | 10 m | Completa (Sen2Cor) |
| 2 | Sentinel-2 **L1C** | **FGAI** (azul + verde + roja + NIR) | 10 m | Ninguna (R_TOA) |
| 3 | Sentinel-3 OLCI **OL_1_EFR** | **FGAI** (azul + verde + roja + NIR) | 300 m | Ninguna (R_TOA) |

### Preguntas de investigación
- ¿Introduce la falta de corrección atmosférica errores significativos en la detección de floraciones (comparar escenarios 1 y 2)?
- ¿A partir de qué tamaño de embalse el FGAI de Sentinel-3 es comparable al de Sentinel-2 (escenario 3 vs 1/2)?
- ¿Puede usarse Sentinel-3 (mayor revisita, ~2 días) como sistema de alerta temprana y Sentinel-2 (10 m) para confirmación espacial detallada?
