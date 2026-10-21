# AWS Strands AgentCore Workshop Sandbox

Código de ejemplo en Python para los módulos 1–6 del workshop **Building GenAI applications with AI Agents that reason, decide and act**, ejecutados en un sandbox temporal de AWS Workshop Studio. La documentación de este repositorio está en español.

> Este repositorio es una recopilación personal de los archivos preparados durante el laboratorio. No es un repositorio oficial de AWS ni un producto listo para producción. El sandbox del evento es temporal y sus recursos, nombres y permisos pueden variar.

## Workshop de referencia

- [Catálogo oficial del workshop](https://catalog.workshops.aws/workshops/eb18d538-bf1f-49b9-9747-c474953deee1/en-US)
- Entorno usado: sandbox temporal de AWS Workshop Studio / Builder Center.
- El código espera recursos ya preparados por el laboratorio, como la función Lambda del agente, el bucket de sesiones, la base de conocimiento, Cognito y AgentCore Gateway. No crea esos recursos.

## Qué incluye

| Archivo | Módulo | Contenido principal |
|---|---:|---|
| `module_01_index.py` | 1 | Agente Strands, Amazon Nova Lite en Amazon Bedrock y herramienta local `flight_search`. |
| `module_02_index.py` | 2 | Consulta de pronóstico del tiempo mediante `http_request` y la API del National Weather Service. |
| `module_03_index.py` | 3 | Persistencia de la sesión del agente en Amazon S3 con `S3SessionManager`. |
| `module_04_index.py` | 4 | Recuperación de información mediante la herramienta `retrieve` y la base de conocimiento de Bedrock. |
| `module_05_index.py` | 5 | Herramientas MCP publicadas por AgentCore Gateway, autenticación OAuth y la compatibilidad temporal descrita abajo. |
| `module_06_index.py` | 6 | Agente detrás de una API con respuesta HTTP y sesión asociada al usuario autenticado por Cognito. |

## Cómo se usa en el laboratorio

Estos archivos son versiones sucesivas del handler de Lambda. En cada módulo, el participante copia el archivo indicado en el editor de código de la función Lambda del sandbox y despliega esa versión siguiendo la guía del workshop.

No se ejecutan como una aplicación local independiente: dependen de las bibliotecas y recursos que el laboratorio provisiona en AWS. El entorno debe tener configuradas las variables requeridas por el módulo. Entre ellas pueden estar `SESSIONS_BUCKET`, `KNOWLEDGE_BASE_ID`, `CLIENT_ID`, `CLIENT_SECRET`, `DOMAIN_URL` y `GATEWAY_URL`.

**No pongas valores reales de credenciales en el código ni en Git.** El módulo 5 y el 6 leen `CLIENT_SECRET` del entorno de Lambda. Los archivos de entorno locales están excluidos por `.gitignore`; los valores de acceso del sandbox no forman parte de este repositorio.

## Nota de compatibilidad MCP

La capa Lambda preinstalada para el workshop incluía una versión del SDK MCP anterior a la versión que negociaba la Gateway. Para completar la prueba del laboratorio, `module_05_index.py` y `module_06_index.py` fijan el handshake MCP en `2025-11-25` y lo anuncian en la cabecera HTTP `MCP-Protocol-Version`.

Es un ajuste específico para la combinación de SDK y Gateway observada en ese sandbox, no una solución general ni la recomendación para una implementación nueva. Para un proyecto propio, actualiza y prueba versiones compatibles de MCP y Strands en lugar de depender de este parche.

## Límites y seguridad

- El sandbox tiene tiempo de vida limitado; al terminar el evento, los recursos o credenciales pueden dejar de estar disponibles.
- Los nombres de variables indican qué configuración necesita cada ejemplo; este repositorio no contiene valores secretos.
- El código demuestra el flujo didáctico del workshop. Antes de adaptarlo a otro entorno, revisa identidad y permisos IAM, validación de entradas, manejo de errores, dependencias y observabilidad.
- La herramienta `flight_search` usa datos de muestra escritos en el código; no consulta aerolíneas reales.
- Los módulos 7 y 8 y los artefactos de evidencia del sandbox no están incluidos en esta carpeta.

## Fuentes

El guion y los nombres de módulos siguen el [material del workshop de AWS](https://catalog.workshops.aws/workshops/eb18d538-bf1f-49b9-9747-c474953deee1/en-US). La implementación refleja los ejemplos ejecutados en el sandbox y puede diferir de futuras revisiones del taller.
