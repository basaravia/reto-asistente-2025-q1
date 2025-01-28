# 🚀 Desafío: Construyendo el Futuro de la IA - Orquestador y Asistente Inteligente 🌟

¡Bienvenidos, futuros expertos en Inteligencia Artificial! 👩‍💻👨‍💻  
Este proyecto está diseñado para retar tus habilidades, motivarte a explorar el increíble mundo de los **Modelos de Lenguaje Extensos (LLMs)**, y afinar tus conocimientos en **arquitectura de software escalable**. Queremos que muestres tu creatividad, técnica y capacidad para resolver problemas reales con IA.

## 🎯 Objetivo del Proyecto
Tu misión es desarrollar un sistema de IA compuesto por:
1. **Un Microservicio Orquestador** que identifique las intenciones del usuario y delegue tareas.
2. **Un Microservicio Asistente** que implemente tres funcionalidades clave:
   - Recuperación Aumentada y Generación (RAG).
   - Análisis de un **estado de cuenta** PDF para analizar gastos.
   - Asesor de compras basado en búsquedas web.

Este sistema será una práctica de aplicaciones inteligentes que combinan **IA generativa**, **procesamiento de documentos** y **búsquedas dinámicas**.

## 🛠️ Requisitos del Proyecto

### 1. **Microservicio Orquestador**
- **Función**: Identificar la intención del usuario y delegar las solicitudes al microservicio asistente.
- **Endpoints**:
  - `/orchestrate`: Recibe una entrada del usuario y la clasifica como:
    - **Chat RAG**: Preguntas y respuestas.
    - **Análisis de PDF**: Resumen de gastos en documentos.
    - **Asesor de Compras**: Recomendación de productos y precios.
- **Tecnologías**:
  - Python.
  - Flask para la API REST.
  - Lógica para llamadas HTTP entre servicios.

### 2. **Microservicio Asistente**
- **Función**: Ejecutar las acciones solicitadas por el orquestador.
- **Endpoints**:
  - `/assistant/rag`: Realizar preguntas y respuestas basadas en recuperación aumentada (RAG).
  - `/assistant/analyze-pdf`: Analizar un archivo PDF para identificar gastos.
  - `/assistant/shopping-advisor`: Buscar y recomendar productos con base en criterios del usuario.
- **Tecnologías**:
  - Python.
  - Flask.

### 3. **Pruebas del Sistema**
- Usa herramientas como **Postman** o `curl` para probar los endpoints del orquestador y del asistente.
- Valida que el flujo de comunicación sea correcto entre los microservicios.
- **IMPORTANTE** Guarda las colecciones de POSTMAN

---

## 🌟 Retos Adicionales (Opcionales)
¿Quieres ir más allá? 🏆 Intenta implementar las siguientes mejoras:

1. **Interfaz de Usuario**:
   - Crea un front-end con **Gradio**, **Streamlit** o un **Framework Web** para interactuar con los microservicios.
   
2. **Contenerizar el Sistema**:
   - Convierte los servicios en contenedores Docker independientes.
   - Proporciona un archivo `docker-compose.yml` para orquestar el despliegue.


## 🧪 Arbol del proyecto esperado
### Crea y versiona tu desarrollo

```
project/
│
├── orchestrator/
│   ├── orchestrator.py          # Código del microservicio orquestador
│   ├── Dockerfile               # Dockerfile del orquestador
│   ├── requirements.txt         # Dependencias del orquestador
│   ├── config/                  # Configuración específica del orquestador
│   │   └── .env                 # Variables de entorno del orquestador
│
├── assistant/
│   ├── assistant.py             # Código del microservicio asistente
│   ├── Dockerfile               # Dockerfile del asistente
│   ├── requirements.txt         # Dependencias del asistente
│   ├── config/                  # Configuración específica del asistente
│   │   └── .env                 # Variables de entorno del asistente
│
├── postman/
│   ├── orchestrator_tests.postman_collection.json  # Colección de pruebas para el orquestador
│   ├── assistant_tests.postman_collection.json     # Colección de pruebas para el asistente
│
├── docker-compose.yml           # Archivo para orquestar los contenedores
└── README.md                    # Documentación del proyecto
```

> NOTA: Puedes agregar las carpetas y archivos necesarios para 


---
## 🧪 Ejemplo de Pruebas
### 1. Solicitar una respuesta RAG
```bash
curl -X POST http://localhost:5001/orchestrate -H "Content-Type: application/json" -d '{"input": "Quiero saber más sobre educación financiera."}'
```


