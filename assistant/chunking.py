import fitz
import re
import json
import requests


class Chunking:
    def __init__(self, path: str, max_chunk_size=100, overlap=0):
        self.path = path
        self.max_chunk_size = max_chunk_size  # Tamaño máximo del chunk
        self.overlap = overlap  # Superposición de palabras

    def extract_text_from_pdf(self):
        """Extrae el texto de un archivo PDF y devuelve un diccionario con número de página y chunks."""
        doc = fitz.open(self.path)
        extracted_data = []
        pdf_name = self.path.split("/")[-1]
        
        for page_num, page in enumerate(doc, start=1):
            text = page.get_text("text").strip()
            if text:
                chunks = self.create_chunks(text)
                for chunk in chunks:
                    extracted_data.append({
                        "NombrePdf": pdf_name,
                        "NumPagina": page_num,
                        "Chunk": chunk
                    })
        
        return extracted_data

    def create_chunks(self, text: str):
        """Divide el texto en chunks semánticos manteniendo coherencia con superposición."""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        chunks = []
        current_chunk = ""
        previous_words = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            words = sentence.split()
            
            if len(current_chunk) + len(sentence) <= self.max_chunk_size:
                current_chunk += " " + sentence if current_chunk else sentence
                previous_words = words[-self.overlap:] if self.overlap > 0 and len(words) >= self.overlap else []
            else:
                chunks.append(current_chunk.strip())
                current_chunk = " ".join(previous_words) + " " + sentence
                previous_words = words[-self.overlap:] if self.overlap > 0 and len(words) >= self.overlap else []
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks

    def prepare_for_weaviate(self):
        """Prepara los datos extraídos para hacer un POST a Weaviate."""
        data = self.extract_text_from_pdf()
        
        if not data:
            print(f"⚠️ No se extrajeron datos del archivo {self.path}")
            return [] 

        weaviate_objects = []

        for entry in data:
            weaviate_objects.append({
                "class": "TextosPdf",
                "properties": {
                    "NombrePdf": entry["NombrePdf"],
                    "NumPagina": entry["NumPagina"],
                    "Chunk": entry["Chunk"]
                }
            })

        print(f"✅ Se generaron {len(weaviate_objects)} objetos para Weaviate.")
        return weaviate_objects

