from flask import Flask
from flask_restful import Api
from dotenv import load_dotenv

#Cargar variables de entorno antes de importar los modulos que las usan
load_dotenv()

from OrchestrationAdapter import OrchestrationAdapter
from controller.OrchestrationController import OrchestrationController


app = Flask(__name__)
api = Api(app)

PORT = 8000

orchestration_controller = OrchestrationController()

api.add_resource(OrchestrationAdapter, "/orchestrate",
                 resource_class_kwargs={'orchestration_controller': orchestration_controller})

if __name__ == "__main__":
    print(f"🚀 Flask API iniciando en http://127.0.0.1:{PORT}")
    app.run(host="127.0.0.1", port=PORT, debug=True)