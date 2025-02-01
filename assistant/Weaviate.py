import requests
from chunking import Chunking

WEAVIATE_URL = "http://weaviate:8080"

def get_all_textos_pdf_uuids():
    """Obtiene todos los UUIDs de la clase TextosPdf en Weaviate."""
    url = f"{WEAVIATE_URL}/v1/objects?class=TextosPdf"
    headers = {"Content-Type": "application/json"}

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        uuids = [obj["id"] for obj in data["objects"]]
        return uuids
    else:
        print(f"⚠️ Error al obtener UUIDs: {response.status_code} - {response.text}")
        return []

def delete_all_textos_pdf():
    """Elimina todos los objetos de la clase TextosPdf en Weaviate usando sus UUIDs."""
    uuids = get_all_textos_pdf_uuids()
    
    if not uuids:
        print("⚠️ No hay objetos para eliminar.")
        return
    
    headers = {"Content-Type": "application/json"}

    for uuid in uuids:
        url = f"{WEAVIATE_URL}/v1/objects/{uuid}"
        response = requests.delete(url, headers=headers)

        if response.status_code == 200:
            print(f"✅ Eliminado objeto {uuid}")
        else:
            print(f"⚠️ Error al eliminar {uuid}: {response.status_code} - {response.text}")

def delete_textos_pdf_class():
    """Elimina la clase TextosPdf en Weaviate (borra todos los datos)."""
    url = f"{WEAVIATE_URL}/v1/schema/TextosPdf"
    headers = {"Content-Type": "application/json"}

    response = requests.delete(url, headers=headers)

    if response.status_code == 200:
        print("✅ Clase TextosPdf eliminada correctamente.")
    else:
        print(f"⚠️ Error al eliminar la clase: {response.status_code} - {response.text}")

def create_textos_pdf_class():
    """Crea la clase TextosPdf en Weaviate con la estructura definida."""
    url = f"{WEAVIATE_URL}/v1/schema"
    headers = {"Content-Type": "application/json"}

    schema = {
        "class": "TextosPdf",
        "description": "Clase que almacena fragmentos de texto extraídos de PDFs",
        "vectorizer": "text2vec-transformers",
        "properties": [
            {
                "name": "NombrePdf",
                "description": "Nombre del archivo PDF de origen",
                "dataType": ["text"],
                "moduleConfig": {
                    "text2vec-transformers": {
                        "skip": True
                    }
                }
            },
            {
                "name": "Chunk",
                "description": "Fragmento de texto extraído del PDF",
                "dataType": ["text"],
                "moduleConfig": {
                    "text2vec-transformers": {
                        "skip": False
                    }
                }
            },
            {
                "name": "NumPagina",
                "description": "Número de la página de donde se extrajo el chunk",
                "dataType": ["int"]
            },
            {
                "name": "embedding",
                "description": "Vector de representación del chunk",
                "dataType": ["number[]"]
            }
        ]
    }

    response = requests.post(url, json=schema, headers=headers)

    if response.status_code == 200:
        print("✅ Clase TextosPdf creada correctamente en Weaviate.")
    else:
        print(f"⚠️ Error al crear la clase: {response.status_code} - {response.text}")

def send_all_pdfs_to_weaviate(pdf_files, batch_size=50, max_chunk_size=100, overlap=3):
    """Procesa múltiples archivos PDF y los envía a Weaviate en lotes, con opciones para configurar chunking."""
    all_data = []
    
    for file in pdf_files:
        chunker = Chunking(file, max_chunk_size=max_chunk_size, overlap=overlap)
        all_data.extend(chunker.prepare_for_weaviate())
    
    if not all_data:
        print("⚠️ No hay datos para enviar a Weaviate.")
        return
    
    url = f"{WEAVIATE_URL}/v1/batch/objects"
    headers = {"Content-Type": "application/json"}
    
    for i in range(0, len(all_data), batch_size):
        batch = {"objects": all_data[i:i + batch_size]}
        
        try:
            print(f"Enviando lote {i//batch_size + 1} de {len(all_data)//batch_size + 1} 🚀")
            response = requests.post(url, json=batch, headers=headers)

            if response.status_code == 200:
                print(f"✅ Lote {i//batch_size + 1} enviado exitosamente.")
            else:
                print(f"⚠️ Error al enviar lote {i//batch_size + 1}: {response.status_code} - {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"❌ Error de conexión con Weaviate: {e}")

def get_context(query: str):
    """Obtiene información relevante de Weaviate basada en una consulta."""
    url = f"{WEAVIATE_URL}/v1/graphql"
    headers = {"Content-Type": "application/json"}

    query_payload = {
        "query": f"""
        {{
            Get {{
                TextosPdf(nearText: {{ concepts: ["{query}"] }}, limit: 1) {{
                    chunk
                    nombrePdf
                    numPagina
                }}
            }}
        }}
        """
    }

    try:
        response = requests.post(url, json=query_payload, headers=headers)
        response.raise_for_status()  # Lanza un error si el status_code no es 200
        data = response.json()
        print(data)

        # Validar que TextosPdf no esté vacío
        textos_pdf = data.get("data", {}).get("Get", {}).get("TextosPdf", [])
        if not textos_pdf:
            return "No se encontraron resultados para la consulta.",0,0
        info = textos_pdf[0]
        chunk = info.get("chunk", "Sin información de chunk")
        nombre_pdf = info.get("nombrePdf", "Desconocido")
        num_pagina = info.get("numPagina", "Desconocido")
        return chunk, nombre_pdf, num_pagina
    #    return f"Chunk: {chunk}\nPDF: {nombre_pdf}\nPágina: {num_pagina}"

    except requests.exceptions.RequestException as e:
        return f"Error al conectar con Weaviate: {e}",0,0
    except Exception as e:
        return f"Error procesando la respuesta: {e}",0,0