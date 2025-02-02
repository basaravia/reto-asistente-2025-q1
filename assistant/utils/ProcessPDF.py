import base64
import fitz  # PyMuPDF
import io
import tempfile
import PyPDF2
import ocrmypdf
import os

class ProcessPDF():
    def __init__(self):
        pass

    def get_pdf_info(self, pdf_base64):
        raw_pdf_data = self._extraer_texto_pdf_a_lista(pdf_base64)
        return self._clean_sensitive_data(raw_pdf_data)

    def _extraer_texto_pdf_a_lista(self, pdf_base64):
        """
        Extrae texto de un PDF, aplicando OCR directamente a los bytes de las imágenes
        en memoria, y devuelve una lista de textos.
        """
        try:
            # Decodificar el base64 a bytes
            pdf_bytes = base64.b64decode(pdf_base64)
            
            # Abrir el PDF desde los bytes
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            total_paginas = len(doc)
            lista_textos = []

            for i in range(1, total_paginas - 1):  # Excluyendo primera y última página
                for img in doc.get_page_images(i):
                    try:
                        xref = img[0]
                        base_image = doc.extract_image(xref)
                        image_bytes = base_image["image"]
                        image_ext = base_image["ext"]

                        # Usar io.BytesIO para crear un objeto de archivo en memoria a partir de los bytes
                        imagen_buffer = io.BytesIO(image_bytes)
                        
                        # Usar io.BytesIO para crear un objeto de archivo en memoria a partir de los bytes
                        imagen_buffer = io.BytesIO(image_bytes)

                        # Usar un directorio temporal personalizado para evitar problemas de permisos
                        try:
                            temp_dir = tempfile.mkdtemp()
                            temp_pdf_path = os.path.join(temp_dir, "temp.pdf")

                            # Aplicar OCR directamente al buffer de la imagen en memoria y obtener el PDF como bytes
                            ocrmypdf.ocr(imagen_buffer, temp_pdf_path, output_type='pdf', input_file_is_pdf=False, image_dpi=300)

                            with open(temp_pdf_path, 'rb') as temp_pdf:
                                pdf_bytes = temp_pdf.read()

                        except PermissionError as e:
                            print(f"Error de permisos al crear archivo temporal: {e}")
                            continue # pasar a la siguiente imagen si hay problemas de permisos

                        # Procesar el PDF en bytes y extraer el texto
                        if pdf_bytes:
                            # Usar io.BytesIO para crear un objeto de archivo en memoria para el PDF
                            pdf_buffer = io.BytesIO(pdf_bytes)
                            pdf_reader = PyPDF2.PdfReader(pdf_buffer)
                            num_pages = len(pdf_reader.pages)
                            
                            for page_num in range(num_pages):
                                page = pdf_reader.pages[page_num]
                                text = page.extract_text()
                                lista_textos.append(text)


                    except Exception as e:
                        print(f"Error al procesar imagen {xref} de la página {i+1}: {e}")
            return lista_textos
        except Exception as e:
            print(f"Error al abrir el pdf: {e}")
            return []

    def _clean_sensitive_data(self, lista_de_textos):
        list_clean = []
        for texto_completo in lista_de_textos:
            partes = texto_completo.split("DETALLE  DE MOVIMIENTOS")

            # La segunda parte de la lista `partes` contiene el texto después de la división
            texto_despues = partes[1] if len(partes) > 1 else ""
            list_clean.append(texto_despues)

        # Unir todos los fragmentos extraídos en una sola cadena
        texto_unido = "".join(list_clean)
        return texto_unido