from flask import Flask
from flask_restful import Api
from dotenv import load_dotenv

load_dotenv()

from adapters.AnalyzePdfAdapter import AnalyzePdfAdapter
from adapters.RagAdapter import RagAdapter
from adapters.ShoppingAdvisorAdapter import ShoppingAdvisorAdapter

app = Flask(__name__)
api = Api(app)

PORT = 5000

api.add_resource(RagAdapter, "/assistant/rag")
api.add_resource(AnalyzePdfAdapter, "/assistant/analyze-pdf")
api.add_resource(ShoppingAdvisorAdapter, "/assistant/shopping-advisor")

if __name__ == "__main__":
    print(f"🚀 Flask API iniciando en http://127.0.0.1:{PORT}")
    app.run(host="127.0.0.1", port=PORT, debug=True)