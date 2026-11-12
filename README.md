# QuantPay Intelligence

**RobertScience · Financial Intelligence Platform**

Plataforma independiente de inteligencia financiera diseñada para transformar datos de pagos en métricas cuantitativas, señales analíticas y evidencia verificable para apoyar la toma de decisiones.

QuantPay Intelligence combina la integración de PayPal Sandbox, el análisis cuantitativo de datos financieros, una capa de inteligencia artificial explicable y visualizaciones financieras. Su objetivo es construir una experiencia fintech ejecutiva en la que los pagos, las métricas y las conclusiones analíticas puedan relacionarse y verificarse.

> **Estado del proyecto:** desarrollo local en curso. La aplicación Flask, el motor cuantitativo inicial, la validación de archivos y las rutas de PayPal Sandbox están implementados. La integración de Gemini AI Insights existe para el análisis de archivos; la ruta financiera independiente `/api/ai/insights` cuenta con una prueba simulada, pero su integración real con Gemini todavía requiere validación. La capa de visualizaciones financieras con Plotly continúa en desarrollo. El flujo completo de pago a captura necesita validación de extremo a extremo. La respuesta de carga CSV incorpora evidencia de integridad SHA-256 y su cálculo se valida mediante pruebas automatizadas.

**Las métricas de demostración utilizan datos sintéticos. No representan transacciones reales de PayPal.**

---

## 1. Objetivo del proyecto

Desarrollar una solución competitiva para el PayPal AI Hackathon que conecte el ciclo de pagos con una capa de inteligencia financiera.

El producto busca responder preguntas como:

- ¿Cuánto dinero representan las operaciones registradas?
- ¿Cuál es el importe promedio por transacción?
- ¿Qué operaciones concentran una mayor proporción del volumen?
- ¿Qué patrones o valores atípicos pueden identificarse en los datos?
- ¿Qué conclusiones se pueden respaldar con métricas verificables?
- ¿Cómo puede conservarse evidencia de la integridad de un reporte analítico?
- ¿Cómo puede utilizarse la inteligencia artificial para explicar resultados cuantitativos sin inventar datos?

La prioridad del producto es **PayPal como núcleo de pagos**, acompañado de analítica cuantitativa, inteligencia explicativa, visualización y trazabilidad.

---

## 2. Visión del producto

QuantPay Intelligence se organiza en cinco capacidades.

### 2.1. PayPal Sandbox

Integración con el entorno de pruebas de PayPal para crear órdenes, consultar sus estados, capturar órdenes aprobadas y consultar sus capturas.

El objetivo es validar el ciclo de pago sin utilizar transacciones reales.

### 2.2. Quantitative Analytics

Cálculo de métricas financieras, distribución de importes, concentración, escenarios y detección de comportamientos atípicos mediante criterios cuantitativos explícitos.

El análisis debe mantener separadas las métricas observadas, las estimaciones y los escenarios hipotéticos.

### 2.3. AI Insights

Capa de inteligencia destinada a explicar resultados calculados, identificar patrones relevantes y relacionar las conclusiones con evidencia disponible.

El proyecto cuenta con un motor local de reglas explicables y una integración con Gemini para generar AI Insights a partir de resultados cuantitativos del análisis de archivos.

También se ha incorporado en `app.py` una ruta financiera independiente, `POST /api/ai/insights`, que utiliza métricas calculadas por `quant_engine.py`.

Esta nueva ruta pasó una prueba local con una respuesta simulada. La llamada real a Gemini desde esta ruta, su manejo integral de errores y su conexión con la interfaz financiera todavía requieren validación.

### 2.4. Evidence & Integrity

Capa de trazabilidad basada en huellas criptográficas SHA-256 para comprobar la correspondencia entre un contenido y su huella registrada.

**Estado actual: parcialmente implementada.**

- [x] Calcular y devolver la huella SHA-256 del archivo CSV cargado.
- [x] Comprobar mediante una prueba automatizada que la huella coincide con los bytes originales del archivo.
- [ ] Generar reportes financieros con contenido estable y verificable.
- [ ] Conservar las huellas asociadas a cada reporte.
- [ ] Verificar posteriormente la integridad de los reportes y detectar modificaciones.

La huella SHA-256 del CSV está implementada y probada. El sistema integral de generación, conservación y verificación de reportes continúa pendiente.

### 2.5. Executive Dashboard

Interfaz de análisis financiero con una identidad visual ejecutiva inspirada en RobertScience.

La interfaz utiliza negro, grafito, dorado `#C8A24C` y blanco cálido. La experiencia debe mantenerse clara, responsive y adecuada para escritorio, tablet y móvil.

---

## 3. Estado actual del desarrollo

**Fase actual: integración de AI Insights, construcción de la primera capa de visualizaciones financieras y consolidación del backend.**

### 3.1. Implementado y validado parcialmente

- [x] Proyecto independiente en `QuantPayIntelligence`.
- [x] Aplicación web Flask en `app.py`.
- [x] Interfaz inicial con identidad visual grafito, negro, dorado y blanco cálido.
- [x] Ejecución local de Flask.
- [x] Respuesta HTTP 200 de la ruta principal en una prueba anterior.
- [x] Métricas demostrativas calculadas a partir de tres registros sintéticos.
- [x] Funciones iniciales de análisis cuantitativo en `quant_engine.py`.
- [x] Validación de archivos CSV y XLSX mediante `upload_routes.py` y `data_engine.py`.
- [x] Validaciones de entradas financieras inválidas.
- [x] Manejo controlado de archivos XLSX dañados.
- [x] Autenticación OAuth de PayPal Sandbox probada.
- [x] Creación de órdenes PayPal probada.
- [x] Consulta del estado de una orden probada.
- [x] Ruta de captura de órdenes aprobadas implementada.
- [x] Ruta de consulta de capturas implementada.
- [x] Interfaz de checkout integrada con el SDK JavaScript de PayPal.
- [x] Integración de Gemini AI Insights en el flujo de análisis de archivos, según las pruebas previas documentadas.
- [x] Ruta `POST /api/ai/insights` incorporada a `app.py`.
- [x] Importación de `generate_ai_insights` desde `ai_insights.py`.
- [x] Compilación de `app.py` y `ai_insights.py` sin errores en la comprobación más reciente.
- [x] Ruta `/api/ai/insights` registrada con método `POST`.
- [x] Prueba local de la ruta financiera de AI Insights con una función simulada: HTTP 200 y respuesta JSON correcta.
- [x] Carpeta `static/` creada para recursos web.
- [x] Biblioteca local de Plotly preparada para la futura capa de visualización.
- [x] Contenedor inicial para gráficas agregado al bloque de carga financiera, según el estado de desarrollo documentado.
- [x] Copias de seguridad creadas antes de cambios seleccionados.
- [x] Siete pruebas automatizadas de AI Insights y carga de archivos ejecutadas correctamente (`7 tests`, `OK`).
- [x] Validación de archivos CSV con escenarios válidos e inválidos, incluidos errores HTTP 400 y 413.
- [x] Cálculo de una huella SHA-256 para el archivo CSV cargado y comprobación automatizada de su correspondencia con los bytes de entrada.

**Importante:** la presencia de una ruta o función no demuestra por sí sola que el flujo completo esté validado. La prueba simulada de `POST /api/ai/insights` no llamó a Gemini y no confirma la disponibilidad ni la calidad de la respuesta del proveedor.

La captura real de una orden de prueba después de su aprobación continúa pendiente de una prueba integral documentada.

La capa de visualizaciones se encuentra en desarrollo. Plotly está preparado localmente, pero la conexión definitiva entre los resultados del análisis cuantitativo y los gráficos del frontend todavía requiere implementación y validación.

### 3.2. Métricas de demostración

Los siguientes resultados proceden de tres registros ficticios:

| Indicador | Resultado |
|---|---:|
| Volumen total | 844.50 USD |
| Número de transacciones | 3 |
| Ticket promedio | 281.50 USD |
| Mayor transacción | 510.00 USD |
| Menor transacción | 89.50 USD |
| Concentración de la mayor transacción | 60.4% |

Los registros están identificados como `DEMO-001`, `DEMO-002` y `DEMO-003`.

Estos valores son una demostración de la lógica cuantitativa. No deben confundirse con pagos de PayPal ni con datos financieros reales.

### 3.3. Trabajo inmediato

- [ ] Completar la conexión de Plotly con los resultados de `quantitative_analysis`.
- [ ] Generar gráficas de ingresos, costos y utilidad.
- [ ] Mostrar métricas financieras junto con sus visualizaciones.
- [ ] Visualizar concentración y valores atípicos cuando los datos permitan calcularlos.
- [ ] Mostrar evolución temporal únicamente cuando existan fechas válidas.
- [ ] Integrar AI Insights junto a las métricas que fundamentan sus explicaciones.
- [ ] Revisar el manejo de errores de la ruta financiera de AI Insights.
- [ ] Validar la integración real de Gemini en esa ruta al final de la fase de desarrollo.
- [ ] Validar la capa de visualización con un archivo financiero de prueba.
- [ ] Confirmar que los datos cargados permanecen separados de las transacciones PayPal.
- [ ] Mantener la interfaz existente sin afectar el checkout ni las rutas PayPal.

---

## 4. Integración PayPal Sandbox

### 4.1. Autenticación

La aplicación utiliza las siguientes variables de entorno:

- `PAYPAL_CLIENT_ID`
- `PAYPAL_CLIENT_SECRET`

La autenticación OAuth de Sandbox ya se probó correctamente.

Las credenciales deben permanecer fuera del código fuente, los registros compartidos y los archivos públicos.

### 4.2. Funciones del backend

En `app.py` se han identificado estas funciones:

- `paypal_access_token()`
- `paypal_create_order()`
- `paypal_get_order(order_id)`
- `paypal_capture_order(order_id)`

La creación de órdenes utiliza la intención `CAPTURE`, un importe de demostración de `1.00 USD` y una descripción identificable de QuantPay Intelligence Sandbox Demo.

### 4.3. Rutas registradas

| Método | Ruta | Responsabilidad |
|---|---|---|
| POST | `/api/paypal/order` | Crear una orden de Sandbox. |
| GET | `/api/paypal/order/<order_id>` | Consultar el estado, importe y moneda de una orden. |
| POST | `/api/paypal/order/<order_id>/capture` | Verificar la aprobación e intentar capturar la orden. |
| GET | `/api/paypal/order/<order_id>/captures` | Consultar las capturas asociadas a una orden. |

### 4.4. Evidencia de pruebas existentes

- La obtención del token OAuth funcionó.
- La creación de una orden devolvió HTTP 201.
- La respuesta de creación incluyó una URL de aprobación.
- La consulta de una orden devolvió HTTP 200.
- Se observó el estado inicial `CREATED` y el importe `1.00 USD`.
- Las funciones y rutas de captura y consulta de capturas están presentes.

### 4.5. Validación integral pendiente

El siguiente flujo debe completarse y documentarse:

1. Crear una orden de prueba.
2. Abrir su URL de aprobación.
3. Aprobarla con una cuenta de prueba de PayPal.
4. Confirmar que PayPal devuelve el estado `APPROVED`.
5. Solicitar la captura desde el backend.
6. Comprobar el resultado de la captura.
7. Consultar la orden y su lista de capturas.
8. Verificar el estado mostrado en el frontend.

Todas estas operaciones deben permanecer en Sandbox. No se necesitan pagos reales.

---

## 5. Motor de análisis cuantitativo

### 5.1. Funciones identificadas

`quant_engine.py` contiene funciones de análisis cuantitativo, entre ellas:

- `analyze_dataset(data)`
- `analyze_financials(revenue, costs, cost_increase_pct=0, revenue_change_pct=0)`
- `generate_ai_insights(analysis)`, según la estructura documentada previamente.

La implementación separa parte de la lógica cuantitativa de la interfaz Flask.

**Nota de arquitectura:** la función `generate_ai_insights` de `quant_engine.py` y las funciones del módulo `ai_insights.py` deben distinguirse por su módulo y responsabilidad. La ruta financiera incorporada en `app.py` utiliza `generate_ai_insights` importada desde `ai_insights.py`.

### 5.2. Capacidades existentes

El análisis financiero contempla:

- Ingresos.
- Costos.
- Utilidad.
- Margen.
- Escenarios de variación de ingresos y costos.
- Concentración de importes.
- Identificación de valores atípicos.
- Explicaciones mediante reglas locales.
- Análisis temporal cuando existen fechas válidas.

La funcionalidad debe seguir evolucionando a partir de resultados cuantitativos verificables, sin inventar métricas ni confundir escenarios hipotéticos con resultados observados.

### 5.3. Validación de desbordamiento

Se incorporó una comprobación de valores no finitos para detectar totales financieros fuera del rango numérico permitido.

En una prueba extrema con ingresos `[1e308, 1e308]` y costos `[1.0, 1.0]`, el sistema rechazó el resultado con un `ValueError` controlado.

También se comprobó un caso normal con:

- Ingresos: `1000.0`.
- Costos: `600.0`.
- Utilidad: `400.0`.
- Margen: `40.0%`.

La compilación de `quant_engine.py` pasó en la prueba documentada. El caso extremo produjo un aviso numérico antes del rechazo controlado, por lo que todavía puede mejorarse ese comportamiento.

---

## 6. Carga y validación de archivos

La ruta `POST /api/data/upload` está implementada en `upload_routes.py`.

La carga se utiliza para analizar datos financieros de forma independiente de las transacciones PayPal.

### Validaciones documentadas

- Archivo obligatorio.
- Extensiones admitidas: CSV y XLSX.
- Tamaño máximo: 10 MB.
- Máximo de 100.000 filas.
- Máximo de 100 columnas.
- Rechazo de columnas vacías o duplicadas.
- Columnas requeridas: `ingresos` y `costos`.
- Rechazo de valores no numéricos.
- Rechazo de valores negativos.
- Rechazo de NaN e infinitos.
- Rechazo de archivos vacíos o sin filas.
- Rechazo de ingresos totales menores o iguales a cero.
- Manejo controlado de archivos XLSX dañados.

Se probaron escenarios válidos e inválidos y se registraron respuestas de error controladas, incluidos errores HTTP 400 para entradas no válidas.

La carga de archivos no debe modificar órdenes ni capturas de PayPal.

---

## 7. AI Insights

AI Insights constituye la capa de inteligencia explicativa de QuantPay Intelligence.

El proyecto cuenta con un motor local de reglas y una integración de Gemini para generar explicaciones a partir de resultados cuantitativos del análisis de archivos.

También se ha agregado una ruta independiente para solicitar análisis financiero mediante el módulo `ai_insights.py`.

### 7.1. Módulo de inteligencia artificial

El archivo `ai_insights.py` expone las funciones:

- `generate_ai_insights(financial_metrics)`
- `generate_uploaded_data_insights(quantitative_analysis)`

Estas funciones están destinadas a recibir métricas calculadas y generar explicaciones en español mediante el proveedor de IA configurado.

La integración utiliza la variable de entorno `GEMINI_API_KEY`. La credencial no debe incluirse en el código fuente, el README ni los registros compartidos.

### 7.2. Endpoint financiero

**Ruta:** `POST /api/ai/insights`

El endpoint incorporado en `app.py`:

1. Ejecuta el análisis financiero de demostración mediante `quant_engine.analyze_financials()`.
2. Prepara las métricas financieras para la función de inteligencia artificial.
3. Llama a `generate_ai_insights(financial_metrics)`.
4. Devuelve la respuesta en formato JSON.
5. Utiliza HTTP 200 cuando el resultado indica éxito y HTTP 503 cuando el resultado indica fallo.

El cálculo financiero utiliza actualmente valores de demostración configurados en el endpoint. No debe interpretarse como un análisis de transacciones reales.

### 7.3. Estado de validación

- [x] Módulo `ai_insights.py` disponible.
- [x] Función de generación de AI Insights financieros disponible.
- [x] Función de análisis de datos cargados disponible.
- [x] Importación de la función financiera en `app.py`.
- [x] Endpoint `POST /api/ai/insights` registrado.
- [x] Compilación de `app.py` y `ai_insights.py` sin errores en la comprobación documentada.
- [x] Respuesta simulada del endpoint validada con HTTP 200.
- [x] Prueba simulada realizada sin llamar a Gemini.
- [ ] Revisar y mejorar el manejo de excepciones del endpoint.
- [ ] Validar la respuesta real de Gemini desde la ruta financiera.
- [ ] Comprobar errores de autenticación, límites y falta de disponibilidad del proveedor.
- [ ] Conectar el endpoint con la interfaz visual.
- [ ] Presentar los resultados junto a las métricas que fundamentan sus explicaciones.
- [ ] Mostrar estados de carga, éxito y error.
- [ ] Completar las pruebas integrales y de regresión.

**La prueba simulada no constituye una validación de la integración real con Gemini.** La llamada real de la nueva ruta se realizará durante la fase final de pruebas para evitar solicitudes externas innecesarias durante el desarrollo.

La IA debe actuar como una capa complementaria de inteligencia financiera. Sus explicaciones deben estar vinculadas a datos disponibles, distinguir hechos de hipótesis y evitar afirmaciones que no puedan respaldarse con las métricas calculadas.

---

## 8. Visualizaciones financieras

La primera capa de visualización se encuentra actualmente en desarrollo.

El objetivo es transformar los resultados cuantitativos ya calculados por el backend en representaciones visuales sin duplicar ni recalcular la lógica financiera en el frontend.

### 8.1. Tecnología

Se utiliza Plotly para la representación gráfica en el navegador.

La biblioteca JavaScript de Plotly se ha preparado localmente dentro de:

`static/plotly.min.js`

La aplicación Flask utiliza su directorio estático estándar para servir recursos web.

### 8.2. Visualizaciones previstas

La capa deberá contemplar, cuando los datos sean suficientes:

- Ingresos.
- Costos.
- Utilidad.
- Margen financiero.
- Concentración de ingresos.
- Distribución de importes.
- Valores atípicos.
- Evolución temporal.

### 8.3. Principios de visualización

Las gráficas deben:

- Utilizar únicamente datos calculados o validados por el backend.
- No inventar fechas ni valores.
- No presentar escenarios hipotéticos como resultados observados.
- Mostrar evolución temporal solamente cuando existan fechas válidas.
- Mantener separados los datos importados de los datos PayPal.
- Mantener disponibles las métricas numéricas aunque una gráfica no pueda generarse.
- Evitar afectar el funcionamiento del checkout de PayPal.
- Mantener la identidad visual ejecutiva de RobertScience.

### 8.4. Estado actual

- [x] Biblioteca Plotly preparada localmente.
- [x] Contenedor inicial para las gráficas agregado al bloque de carga financiera, según el estado de desarrollo registrado.
- [ ] Confirmar que el navegador carga correctamente la biblioteca local.
- [ ] Conectar la respuesta de `/api/data/upload` con las gráficas.
- [ ] Implementar gráfica de ingresos, costos y utilidad.
- [ ] Implementar concentración y valores atípicos cuando corresponda.
- [ ] Implementar serie temporal cuando el análisis temporal sea válido.
- [ ] Integrar las gráficas con AI Insights.
- [ ] Validar visualmente los resultados con un archivo financiero de prueba.
- [ ] Ejecutar pruebas de regresión después de completar la capa.

**La capa de visualización todavía no debe considerarse terminada.**

---

## 9. Evidence & Integrity — SHA-256

La capa de integridad se encuentra parcialmente implementada.

### 9.1. Evidencia SHA-256 en la carga de archivos

La ruta `POST /api/data/upload` incorpora una huella SHA-256 del archivo CSV cargado en la respuesta de evidencia.

- [x] Calcular la huella SHA-256 del archivo CSV recibido.
- [x] Incluir la huella en la evidencia devuelta por la carga.
- [x] Validar mediante una prueba automatizada que la huella coincide con los bytes originales del archivo de prueba.

La validación forma parte de la suite automatizada de siete pruebas que terminó con resultado `OK`.

### 9.2. Integridad completa de reportes — pendiente

La implementación de un sistema integral de reportes verificables sigue pendiente:

- [ ] Definir qué datos y resultados integran cada reporte.
- [ ] Generar una representación estable del contenido del reporte.
- [ ] Calcular la huella SHA-256 de esa representación.
- [ ] Conservar la huella junto con una referencia al reporte.
- [ ] Verificar posteriormente si el contenido coincide con la huella registrada.
- [ ] Probar la detección de modificaciones.
- [ ] Documentar los límites de la comprobación.

### 9.3. Alcance y limitaciones

Una huella SHA-256 permite detectar diferencias entre un contenido y la huella calculada para él, siempre que exista una referencia de confianza para la comparación. Por sí sola, no demuestra la legitimidad de un pago, la autenticidad del origen de los datos ni la identidad de quien generó un reporte.

**Estado:** la evidencia SHA-256 en la carga CSV está implementada y probada. La generación y verificación integral de reportes continúa pendiente.

## 10. Arquitectura del proyecto

### Archivos identificados actualmente

- `app.py`: aplicación Flask, interfaz web, checkout y rutas PayPal, incluida la nueva ruta financiera de AI Insights.
- `ai_insights.py`: funciones de generación de inteligencia artificial para métricas financieras y análisis de datos cargados.
- `upload_routes.py`: endpoint de carga de archivos.
- `data_engine.py`: lectura y validación de datos.
- `quant_engine.py`: análisis cuantitativo y lógica analítica.
- `README.md`: documentación del proyecto.
- `static/plotly.min.js`: biblioteca local de Plotly preparada para las visualizaciones.
- `head.jpg` a `head5.jpg`: recursos gráficos existentes.
- Archivos de respaldo y scripts auxiliares creados durante el desarrollo.

### Evolución prevista

La estructura puede ampliarse cuando exista una necesidad técnica concreta:

- `analytics/`: lógica analítica, si conviene organizarla como paquete.
- `templates/` y `static/`: plantillas y recursos web, si se justifica separarlos de `app.py`.
- `tests/`: pruebas automatizadas.
- `requirements.txt`: dependencias reproducibles.
- `.env.example`: nombres de variables de configuración sin secretos.
- `.gitignore`: exclusión de credenciales, entornos y archivos locales.
- `README.md`: instrucciones y estado actualizado.

La reorganización no es una prioridad inmediata. Se preservará la implementación existente y se evitarán refactorizaciones innecesarias.

---

## 11. Entorno de desarrollo

- Python 3.11.9.
- Flask 2.3.3, versión registrada en el entorno actual.
- Entorno virtual compartido existente: `quant-laboratory`.
- Ejecución local: `python app.py`.
- Dirección local: `http://127.0.0.1:5000`.

Activación del entorno en PowerShell:

```powershell
& "C:\Dev\quant-laboratory\Scripts\Activate.ps1"
```

Ruta del proyecto:

```text
C:\Users\Rober\OneDrive\Documentos\projects\QuantPayIntelligence
```

El entorno virtual compartido se utiliza para desarrollo y pruebas. No se debe crear ni incorporar un entorno virtual dentro de la carpeta del proyecto.

La distribución final deberá documentar y fijar las dependencias necesarias para reproducir la aplicación en un entorno limpio.

---

## 12. Seguridad y separación de proyectos

QuantPay Intelligence es independiente de los demás sistemas de RobertScience.

Principios obligatorios:

- Mantener todos los cambios dentro de la carpeta de este proyecto.
- No modificar la web principal de RobertScience ni VÉRA.
- Utilizar el entorno `quant-laboratory` para desarrollo y pruebas.
- No instalar paquetes sin necesidad demostrada.
- Mantener las credenciales fuera del código.
- No imprimir ni compartir valores de secretos o claves API.
- Utilizar datos sintéticos claramente identificados.
- Realizar pruebas de pagos únicamente en Sandbox.
- Evitar llamadas externas innecesarias durante el desarrollo.
- Crear respaldos antes de editar archivos existentes.
- Verificar los cambios sin ejecutar pruebas redundantes.
- No afirmar que una capacidad funciona sin evidencia reproducible.
- No publicar ni desplegar sin autorización explícita.

La publicación, la creación de un repositorio remoto y el despliegue requieren autorización expresa mediante **LUZ VERDE**.

---

## 13. Plan de trabajo

### Prioridad 1 — Completar AI Insights y visualizaciones

- [x] Incorporar la ruta financiera `POST /api/ai/insights`.
- [x] Verificar que la ruta está registrada.
- [x] Comprobar la compilación de los módulos implicados.
- [x] Probar el endpoint con una respuesta simulada sin llamar a Gemini.
- [ ] Revisar el manejo de errores del endpoint financiero.
- [ ] Confirmar el contrato de respuesta JSON.
- [ ] Conectar Plotly con los resultados del análisis cuantitativo.
- [ ] Crear gráficas de ingresos, costos y utilidad.
- [ ] Mostrar márgenes financieros cuando los datos permitan calcularlos.
- [ ] Visualizar concentración, distribución y valores atípicos cuando corresponda.
- [ ] Mostrar evolución temporal solo cuando existan fechas válidas.
- [ ] Presentar Gemini AI Insights junto a las métricas que fundamentan sus explicaciones.
- [ ] Incorporar estados de carga, éxito y error.
- [ ] Mantener separados los pagos, los datos sintéticos y los archivos importados.
- [ ] Validar visualmente el resultado con archivos de prueba.
- [ ] Ejecutar pruebas de regresión.

### Prioridad 2 — Validar la integración real de Gemini

- [ ] Ejecutar una prueba real de `POST /api/ai/insights` cuando termine la integración.
- [ ] Comprobar la estructura de la respuesta del proveedor.
- [ ] Revisar errores de autenticación, límites y tiempos de espera.
- [ ] Verificar que las explicaciones se basan en las métricas proporcionadas.
- [ ] Documentar resultados y limitaciones.

Las llamadas reales a Gemini deben concentrarse en la fase final de pruebas, evitando solicitudes innecesarias durante los cambios de interfaz.

### Prioridad 3 — Cerrar PayPal Sandbox

- [ ] Revisar el JavaScript del checkout.
- [ ] Aprobar una orden de prueba.
- [ ] Capturar la orden desde el backend.
- [ ] Verificar el resultado y las capturas.
- [ ] Comprobar mensajes de éxito y error.
- [ ] Conectar las operaciones confirmadas con las métricas del dashboard.

### Prioridad 4 — Pruebas y robustez

- [ ] Crear pruebas automatizadas para el motor cuantitativo.
- [ ] Probar rutas Flask y estados de PayPal.
- [ ] Cubrir errores de red y respuestas inválidas.
- [ ] Revisar la validación de datos.
- [ ] Ejecutar pruebas de regresión tras cada cambio relevante.
- [ ] Documentar las pruebas integrales con sus resultados reales.

### Prioridad 5 — Integridad y trazabilidad

- [x] Calcular la huella SHA-256 del archivo CSV cargado.
- [x] Validar mediante pruebas automatizadas que la huella coincide con los bytes originales.
- [ ] Definir el contenido y formato estable de los reportes financieros.
- [ ] Conservar las huellas SHA-256 asociadas a los reportes.
- [ ] Implementar y probar la verificación posterior de integridad.
- [ ] Documentar qué garantiza y qué no garantiza una huella criptográfica.

### Prioridad 6 — Experiencia y entrega

- [ ] Revisar la interfaz en escritorio, tablet y móvil.
- [ ] Consolidar el diseño ejecutivo RobertScience.
- [ ] Actualizar instrucciones de instalación y ejecución.
- [ ] Preparar un entorno limpio y reproducible.
- [ ] Revisar secretos y archivos antes de publicar.
- [ ] Preparar la demostración integral.
- [ ] Completar la documentación de Devpost.
- [ ] Crear y publicar el repositorio solo con autorización.
- [ ] Preparar un video público de demostración de menos de tres minutos.
- [ ] Completar la entrega antes de la fecha límite aplicable.

---

## 14. Criterio de aceptación

Una funcionalidad solo se considerará completada cuando:

1. Esté implementada.
2. Tenga una prueba adecuada.
3. Produzca resultados reproducibles.
4. Se haya comprobado que no rompe funcionalidades existentes.
5. Su documentación describa fielmente su alcance y limitaciones.

La existencia de una ruta, función o elemento visual no es suficiente para declarar validado un flujo completo.

Las pruebas simuladas deben identificarse como tales y no deben utilizarse como evidencia de una integración real con un proveedor externo.

---

## 15. Registro de continuidad

**Última actualización:** 28 de octubre de 2026.

**Estado general:** prototipo local en evolución. El proyecto dispone de una interfaz inicial, un motor cuantitativo, validación de archivos, integración de Gemini AI Insights en el flujo de análisis de archivos y rutas PayPal Sandbox. La ruta financiera `POST /api/ai/insights` está registrada y pasó una prueba local simulada, pero su integración real con Gemini sigue pendiente de validación. La captura de órdenes PayPal después de su aprobación necesita una prueba integral documentada. La primera capa de visualizaciones financieras con Plotly continúa en desarrollo.

**Último avance comprobado:**

- La suite `test_ai_insights_local` terminó con siete pruebas aprobadas (`7 tests`, `OK`).
- Se validaron escenarios de carga CSV válidos e inválidos, incluidos errores HTTP 400 y 413.
- Una prueba automatizada comprobó que la huella SHA-256 devuelta para el CSV coincide con los bytes originales del archivo de prueba.
- La respuesta de carga incorpora evidencia de integridad SHA-256.
- La ruta financiera de AI Insights pasó una prueba con una función simulada. Esa prueba no llamó a Gemini ni demuestra que la integración real con el proveedor funcione.
- La compilación de los módulos implicados pasó en las comprobaciones documentadas previamente.

**Advertencia de pruebas:** durante la ejecución completa de la suite aparece intermitentemente un `ResourceWarning` relacionado con un archivo temporal utilizado en la codificación multipart de Werkzeug. Las siete pruebas siguen terminando correctamente, pero el origen del aviso aún no se ha aislado. No debe considerarse resuelto ni atribuirse definitivamente a un defecto de la aplicación sin más evidencia.

**Estado de Evidence & Integrity:** la huella SHA-256 del archivo CSV está implementada y probada. La generación de reportes verificables, el registro persistente de sus huellas y la comprobación posterior de modificaciones siguen pendientes.

**Estado de visualizaciones:** Plotly está preparado localmente y existe un contenedor inicial para las gráficas, según el estado documentado. La conexión entre los resultados de `POST /api/data/upload`, las métricas cuantitativas y las visualizaciones todavía requiere implementación y validación en el navegador.

**Siguiente paso de desarrollo:** continuar con la conexión de las métricas financieras a Plotly y la interfaz de AI Insights, revisar el manejo de errores y conservar las pruebas existentes. Después, validar la integración real con Gemini y completar las pruebas integrales de PayPal Sandbox cuando corresponda.

**Reglas de continuidad:** trabajar con un solo comando por turno, realizar cambios mínimos, conservar respaldos y mantener el trabajo aislado en `QuantPayIntelligence`. No modificar RobertScience ni VÉRA, no instalar dependencias sin necesidad demostrada y no publicar ni desplegar sin autorización explícita mediante **LUZ VERDE**.