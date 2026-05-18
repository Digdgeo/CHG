# Guía paso a paso: crear una cuenta para Google Earth Engine

> Documento dirigido a alumnos sin experiencia previa con Google Earth Engine (GEE) ni con Google Cloud. Sigue los pasos en orden; el proceso completo lleva entre 10 y 20 minutos.

---

## 0. ¿Qué vamos a hacer y por qué tantos pasos?

Google Earth Engine es la plataforma de Google para procesar imágenes de satélite y datos geoespaciales en la nube. Desde noviembre de 2024, Google ha integrado GEE dentro de su ecosistema Google Cloud Platform, así que **ya no basta con tener una cuenta de Gmail**: hace falta también un "proyecto de Google Cloud" vinculado a esa cuenta, que actúa como el espacio de trabajo donde GEE registra tu actividad.

En resumen, para acceder a GEE necesitas tres cosas en este orden:

1. Una **cuenta de Google** (cualquier Gmail vale).
2. Un **proyecto de Google Cloud** asociado a esa cuenta.
3. Ese proyecto **registrado para uso no comercial** en Earth Engine, con un *tier* de cuota seleccionado.

Para uso académico no comercial **todo es gratuito** y **no se pide tarjeta de crédito** en ningún momento. Si alguna pantalla te pide datos de facturación, algo se ha torcido — vuelve atrás.

---

## 1. Cuenta de Google

Si ya tienes Gmail, salta al paso 2.

1. Entra en [https://accounts.google.com/signup](https://accounts.google.com/signup).
2. Rellena el formulario (nombre, fecha de nacimiento, etc.).
3. Elige un nombre de usuario. **Recomendación**: usa un correo que vayas a mantener (personal o institucional); todos los datos, scripts y proyectos de GEE quedarán asociados a él.
4. Verifica con el SMS que te llega al móvil.
5. Acepta las condiciones.

**¿Cuenta personal (`@gmail.com`) o institucional (`@csic.es`, `@us.es`, etc.)?** Si tu institución gestiona Google Workspace, la institucional funciona, pero a veces el administrador IT restringe la creación de proyectos en Google Cloud y te puedes quedar atascado en el paso 3. Para un curso, lo más seguro es **una cuenta `@gmail.com` personal**: evita problemas y la podrás seguir usando después del curso.

---

## 2. Acceder al portal de registro de Earth Engine

1. Abre el navegador (Chrome o Firefox van bien; evita Internet Explorer y Edge en modo antiguo).
2. Asegúrate de estar logueado en Google con la cuenta del paso 1. Lo compruebas mirando el icono de tu avatar arriba a la derecha en cualquier página de Google.
3. Ve a: **[https://code.earthengine.google.com/register](https://code.earthengine.google.com/register)**
4. Si es la primera vez, te pedirá aceptar los **Términos de Servicio de Google Cloud**. Léelos por encima y acepta.

> ⚠️ Si te aparece un mensaje del tipo *"Your organization doesn't allow you to create projects"* es que estás usando una cuenta institucional con restricciones. Cierra sesión y entra con una cuenta `@gmail.com` personal.

---

## 3. Crear y registrar el proyecto de Google Cloud

Al entrar en la página de registro, te guía un asistente con varios pasos. Vamos paso por paso.

### 3.1. Elegir el tipo de uso

Te preguntará para qué vas a usar Earth Engine. Selecciona:

- **Unpaid usage** (uso no remunerado / no comercial)
- Y dentro de las subcategorías: **Academia & Research** (o **Education**, si te aparece la opción).

### 3.2. Confirmar elegibilidad no comercial

Te hará un breve cuestionario para verificar que cumples los requisitos de uso no comercial:

- **Tu rol**: selecciona *Student* o *Participant*.
- **Institución**: nombre de tu universidad o centro (ej. *Universidad de Sevilla*, *CSIC – Estación Biológica de Doñana*).
- **Descripción del trabajo**: algo breve, por ejemplo:
  > "Aprendizaje de teledetección y análisis de imágenes satélite en el marco de un curso de formación universitaria."
- **Fechas**: pon como fecha de inicio la del curso y como fin una fecha razonable (puedes poner +1 año tranquilamente).

Pulsa **Check eligibility** y debería aparecer un mensaje confirmando que eres elegible para uso no comercial.

### 3.3. Crear el proyecto

Ahora te pide crear (o seleccionar) un proyecto de Google Cloud:

- **Project name**: pon algo descriptivo. **Convención recomendada por Google**: `ee-tunombre` (por ejemplo `ee-luciamartinez`, `ee-juanperez23`). Si el nombre ya está cogido, añade números al final.
- **Organization** y **Location**: si estás con cuenta personal `@gmail.com`, selecciona **No Organization**. Si es institucional, aparecerá tu institución; déjala como está.

Pulsa **Continue**.

### 3.4. Elegir el *tier* (nivel de cuota)

Aquí te aparece la novedad de 2026: los niveles de cuota de cómputo. Verás tres opciones:

| Tier | Cuota mensual | Requisitos | Cuándo elegirlo |
|---|---|---|---|
| **Community** | Cuota básica | Ninguno | **Esto es lo que tienes que elegir** para el curso |
| **Contributor** | Cuota intermedia | Cuenta de facturación (para identificación, no para cobrar) | Más adelante, si te quedas corto |
| **Partner** | Cuota alta | Solicitud justificada (ONG, gobierno, investigación de alto impacto) | No aplica a estudiantes |

**Selecciona Community Tier**. Para aprender y para hacer los ejercicios del curso sobra. Si en el futuro necesitas más, puedes subir de tier desde la consola sin tener que reconfigurar nada.

### 3.5. Confirmar y registrar

- Revisa el resumen.
- Pulsa **Register**.
- Te llevará a una pantalla donde tienes que pulsar **Enable API** para activar la API de Earth Engine sobre el proyecto. Pulsa **Enable**.
- Cuando termine (unos segundos), ya está. Tu proyecto está registrado y listo.

---

## 4. Comprobar que todo funciona: entrar al Code Editor

1. Ve a **[https://code.earthengine.google.com/](https://code.earthengine.google.com/)**.
2. Arriba a la derecha verás el nombre del proyecto que acabas de crear (ej. `ee-tunombre`). Si por algún motivo aparece otro o ninguno, pulsa en tu avatar → **Change Cloud Project** y selecciónalo.
3. En el panel central (editor de código), copia y pega este script de prueba:

   ```javascript
   // Test mínimo: muestra una imagen Sentinel-2 sobre Sevilla
   var punto = ee.Geometry.Point([-5.9845, 37.3891]);
   var imagen = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
     .filterBounds(punto)
     .filterDate('2024-06-01', '2024-09-30')
     .sort('CLOUDY_PIXEL_PERCENTAGE')
     .first();

   Map.centerObject(punto, 11);
   Map.addLayer(imagen, {bands: ['B4','B3','B2'], min: 0, max: 3000}, 'Sentinel-2 RGB');
   print('Metadatos de la imagen:', imagen);
   ```

4. Pulsa **Run** (botón arriba del editor, o `Ctrl + Enter`).
5. En unos segundos deberías ver una imagen Sentinel-2 de Sevilla en el mapa y los metadatos en la pestaña **Console**.

Si lo ves: **enhorabuena, tu cuenta funciona**. Ya puedes empezar a trabajar.

---

## 5. Problemas frecuentes y cómo resolverlos

### "No puedo crear el proyecto / me sale error de permisos"
Estás con una cuenta institucional cuyo administrador no permite crear proyectos en Google Cloud. Solución: usa una cuenta `@gmail.com` personal.

### "Me pide tarjeta de crédito en algún paso"
Algo se ha torcido. Para uso no comercial **nunca** se pide tarjeta. Comprueba que:
- Has elegido **Unpaid usage** y no **Paid usage**.
- En el cuestionario de elegibilidad seleccionaste *Academia / Research / Education*.
- En el tier elegiste **Community** y no Contributor (este sí pide cuenta de facturación, aunque tampoco cobra).

Si todo eso está bien y aun así te lo pide, vuelve al inicio y empieza otra vez con un nombre de proyecto diferente.

### "El Code Editor no carga / aparece pantalla en blanco"
- Cierra sesión y vuelve a entrar.
- Prueba en una ventana de incógnito (a veces las extensiones del navegador dan guerra).
- Comprueba que no tienes activo ningún bloqueador agresivo (uBlock, Privacy Badger) en `earthengine.google.com`.

### "Aparece un mensaje sobre selección de tier obligatoria antes del 27 de abril de 2026"
Es normal. Significa que aún no has elegido tier. Vuelve al paso 3.4: ve a la consola de Google Cloud → Earth Engine → Manage Tier y selecciona Community.

### "He creado dos proyectos sin querer"
No pasa nada. Puedes borrar el que no quieras desde [https://console.cloud.google.com/](https://console.cloud.google.com/) → IAM y administración → Gestión de recursos → seleccionar el proyecto → Eliminar. Eso sí, asegúrate de no borrar el que sí estás usando.

### "Mi proyecto aparece como 'pendiente de verificación' o 'on hold'"
Si registraste el proyecto antes del 15 de abril de 2025, Google pide reverificar la elegibilidad no comercial. Ve a la consola de Cloud → Earth Engine → Configuration y rellena de nuevo el cuestionario.

---

## 6. Recursos adicionales

- **Documentación oficial GEE**: https://developers.google.com/earth-engine
- **Catálogo de datos**: https://developers.google.com/earth-engine/datasets/
- **Tutoriales oficiales**: https://developers.google.com/earth-engine/tutorials
- **Curso gratuito y abierto (en inglés) muy recomendable**: https://courses.spatialthoughts.com/end-to-end-gee.html
- **Foro de la comunidad** (para dudas): https://groups.google.com/g/google-earth-engine-developers

---

## 7. Resumen visual del flujo

```
Cuenta Google (Gmail)
        │
        ▼
Página de registro de GEE  ──►  Aceptar T&C Google Cloud
        │
        ▼
Tipo de uso: NO COMERCIAL  ──►  Rol: Student / Participant
        │
        ▼
Crear proyecto  ──►  Nombre: ee-tunombre  ──►  No organization
        │
        ▼
Elegir tier: COMMUNITY (gratis, sin tarjeta)
        │
        ▼
Register  ──►  Enable API
        │
        ▼
https://code.earthengine.google.com → ¡A trabajar!
```

---

*Última actualización: mayo de 2026. La interfaz de registro de Google Cloud cambia con cierta frecuencia; si algún paso no coincide exactamente con lo que ves en pantalla, el espíritu sigue siendo el mismo: cuenta Google → proyecto → registro no comercial → tier Community → Enable API.*
