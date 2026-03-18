# Teledetección con SNAP y Sentinel

Módulo de introducción a la teledetección con el software SNAP de la ESA e imágenes Sentinel-2 y Sentinel-3.

## Clase 1 — Introducción a SNAP y Sentinel

### Contenidos
- Conceptos básicos de teledetección
- El programa Copernicus y los satélites Sentinel
- Sentinel-2: características, bandas y aplicaciones
- Sentinel-3: características y aplicaciones en tierra y océano
- Descarga de imágenes desde el Copernicus Data Space
- Introducción al software SNAP: interfaz y herramientas principales
- Carga, visualización y combinaciones de bandas
- Corrección atmosférica con Sen2Cor (Sentinel-2)

### Software y recursos
- **SNAP 13**: https://step.esa.int/main/download/snap-download/
- **Anaconda**: https://www.anaconda.com/download
- **Copernicus Data Space**: https://dataspace.copernicus.eu/
- **Documentación Sentinel-2**: https://sentinel.esa.int/web/sentinel/missions/sentinel-2
- **Documentación Sentinel-3**: https://sentinel.esa.int/web/sentinel/missions/sentinel-3

---

## Instalación

### 1. Instalar SNAP 13

Descargar el instalador desde https://step.esa.int/main/download/snap-download/ y seguir el asistente de instalación.

### 2. Instalar Anaconda

Descargar el instalador desde https://www.anaconda.com/download y seguir el asistente. Una vez instalado, abrir **Anaconda Prompt** (Windows) o una terminal (Linux/Mac).

Verificar la instalación:

```bash
conda --version
```

### 3. Crear el entorno de trabajo para esa_snappy

A partir de SNAP 10, el módulo de Python se llama **`esa_snappy`** (antes era `snappy`). Crear un entorno limpio de conda **antes** de instalar SNAP:

```bash
conda create -n esa_snappy python=3.10
```

### 4. Configurar esa_snappy durante la instalación de SNAP

El instalador de SNAP 13 incluye un paso donde pide el path del entorno de Python. Basta con indicar la ruta del entorno creado en el paso anterior.

La ruta del entorno suele ser:

**Windows:**
```
C:\Users\<usuario>\anaconda3\envs\esa_snappy
```

**Linux/Mac:**
```
~/anaconda3/envs/esa_snappy
```

### 5. Verificar la instalación

Activar el entorno y comprobar que el módulo carga correctamente:

```bash
conda activate esa_snappy
python -c "import esa_snappy; print(esa_snappy.ProductIO)"
```

Si no da error, la instalación es correcta.

### Plugins SNAP (archivos .nbm)

Los archivos `.nbm` (NetBeans Module) son el formato de paquete de plugins de SNAP, que está construido sobre la plataforma NetBeans. Se instalan desde SNAP en `Tools > Plugins > Downloaded`.

Los plugins necesarios para esta clase están en la carpeta `plugins/`:

| Archivo | Descripción | Fuente |
|---------|-------------|--------|
| `sen2res.nbm` | **Sen2Res** — super-resolución de Sentinel-2: remuestreo/pansharpen de las bandas a 20 m y 60 m hasta 10 m | [step.esa.int](https://step.esa.int/main/snap-supported-plugins/sen2res/) |
| `org-netbeans-modules-javahelp.nbm` | Módulo de ayuda de Java para NetBeans — necesario para resolver un error de instalación de Sen2Res y otros plugins | [Apache NetBeans 14](https://archive.apache.org/dist/netbeans/netbeans/14/nbms/platform/org-netbeans-modules-javahelp.nbm) |

> **Nota:** Si la instalación de Sen2Res falla, instalar primero `org-netbeans-modules-javahelp.nbm` manualmente desde la pestaña *Downloaded* del gestor de plugins.
> Ver hilo del foro: https://forum.step.esa.int/t/plugin-installation-problem-with-sen2res-and-others/44612

### Datos de prácticas
Los datos utilizados en las prácticas se encuentran en el saco del curso, en la carpeta `datos_dia3`.
