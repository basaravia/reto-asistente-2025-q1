from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
from pdfReader.GetPdfDataframe import GetPdfDataframe
from chunking import Chunking
from Weaviate import delete_all_textos_pdf, send_all_pdfs_to_weaviate, delete_textos_pdf_class, create_textos_pdf_class,get_context
from threading import Thread
from graph import GraphWorkflow
from datetime import datetime
from researcher.Researcher import Researcher

app = Flask(__name__)
pipeline = GraphWorkflow()
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/assistant/update-rag', methods=['POST'])
def update_rag():
    """Updates RAG chunking parameters"""
    data = request.json
    batch_size = data.get("batch_size", 70)
    overlap = data.get("overlap", 2)
    max_chunk_size = data.get("max_chunk_size", 1000)

    def process_task():
        try:
            delete_textos_pdf_class()
            create_textos_pdf_class()
            pdf_files = [
                "./data/Capacitación_Norma_de_Educación_Financiera-10dic2024-21.pdf",
                "./data/ed_financiera_cfn.pdf",
                "./data/finanzas_dummies_book.pdf"
            ]
            send_all_pdfs_to_weaviate(pdf_files, batch_size=batch_size, max_chunk_size=max_chunk_size, overlap=overlap)
            print("✅ RAG updated successfully.")
        except Exception as e:
            print(f"❌ Error processing RAG: {e}")

    # Iniciar la tarea en segundo plano
    Thread(target=process_task).start()

    return jsonify({
        "status": "processing",
        "message": "RAG update in progress",
        "parameters": {
            "batch_size": batch_size,
            "overlap": overlap,
            "max_chunk_size": max_chunk_size
        }
    }), 202
@app.route('/assistant/rag', methods=['POST'])
def assistant_rag():
    """Simulación de Recuperación Aumentada con Generación (RAG)"""
    data = request.json
    query = data.get("query", None)
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    response = {
        "query": query,
        "response": f"{pipeline.invoke({'input': query})}",
        "timestamp":datetime.now().isoformat() 
    }
    return jsonify(response)

@app.route('/assistant/analyze-pdf', methods=['POST'])
def analyze_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No se envió ningún archivo"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Nombre de archivo inválido"}), 400
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    try:
        pdf = GetPdfDataframe(filepath)
        gastos,entradas,visitas=pdf.getTables()
        resumen = pdf.resumen(modelo=pipeline.llm,user_input="Resúmenes de gastos y entradas")
        return jsonify({"gastos":gastos,"filename": resumen,"entradas":entradas,"visitas":visitas}), 200
    except Exception as e:
        return jsonify({"Error": "Asegurate de enviar un pdf de un estado de cuenta de Banco Pichincha"}), 500
@app.route('/assistant/shopping-advisor', methods=['POST'])
def shopping_advisor():
    """Asesor de compras basado en preferencias del usuario."""
    data = request.json
    query = data.get("query", False)
    if query:
            return jsonify({"response": Researcher(query).research()})

    
    return jsonify({"error": "verifique la forma de su query"})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
