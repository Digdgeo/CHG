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
- **SNAP**: https://step.esa.int/main/download/snap-download/
- **Copernicus Data Space**: https://dataspace.copernicus.eu/
- **Documentación Sentinel-2**: https://sentinel.esa.int/web/sentinel/missions/sentinel-2
- **Documentación Sentinel-3**: https://sentinel.esa.int/web/sentinel/missions/sentinel-3

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
Los datos utilizados en las prácticas se encuentran en la carpeta `datos/`.
