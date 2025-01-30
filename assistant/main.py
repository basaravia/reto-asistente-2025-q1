from flask import Flask
from flask_restful import Api

from assistant import AnalyzePdfAdapter, RagAdapter, ShoppingAdvisorAdapter

app = Flask(__name__)
api = Api(app)

api.add_resource(RagAdapter, "/assistant/rag")
api.add_resource(AnalyzePdfAdapter, "/assistant/analyze-pdf")
api.add_resource(ShoppingAdvisorAdapter, "/assistant/shopping-advisor")

if __name__ == "__name__":
    app.run(host="172.0.0.1", port=5000, debug=True)