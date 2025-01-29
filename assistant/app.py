from flask import Flask, request, jsonify
import os
import PyPDF2
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Carpeta para subir archivos
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/assistant/rag', methods=['POST'])
def assistant_rag():
    """Simulación de Recuperación Aumentada con Generación (RAG)"""
    data = request.json
    query = data.get("query", "")
    
    # Simulación de respuesta de un sistema RAG
    response = {
        "query": query,
        "response": f"Aquí tienes información relevante sobre: {query}"
    }
    return jsonify(response)

@app.route('/assistant/analyze-pdf', methods=['POST'])
def analyze_pdf():
    """Analiza un archivo PDF y extrae su contenido."""
    if 'file' not in request.files:
        return jsonify({"error": "No se envió ningún archivo"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Nombre de archivo inválido"}), 400
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    # Extraer texto del PDF
    text = ""
    with open(filepath, "rb") as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    
    return jsonify({"filename": filename, "content": text})

@app.route('/assistant/shopping-advisor', methods=['POST'])
def shopping_advisor():
    """Asesor de compras basado en preferencias del usuario."""
    data = request.json
    category = data.get("category", "general")
    budget = data.get("budget", 0)
    
    recommendations = {
        "electronics": ["Smartphone X", "Laptop Y", "Tablet Z"],
        "fashion": ["Zapatos deportivos", "Camisa elegante", "Reloj clásico"],
        "general": ["Cualquier producto de buena calidad dentro de tu presupuesto"]
    }
    
    result = recommendations.get(category, ["Sin recomendaciones disponibles"])
    
    return jsonify({"category": category, "budget": budget, "recommendations": result})

if __name__ == '__main__':
    app.run(debug=True)
