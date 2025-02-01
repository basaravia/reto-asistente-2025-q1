from semantic_router.layer import RouteLayer
import logging
import os
from model.model import Model
from utils.PromptManager import PromptManager
from service.AssistantService import AssistantService

logging.basicConfig(level=logging.DEBUG)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
FILE_PATH = os.path.join(BASE_DIR, "..", "utils", "data", "semantic_router.json")

URL_ASSISTANT = "http://127.0.0.1:5000"

class OrchestrationController():
    def __init__(self):
        self.sr_router = RouteLayer.from_json(FILE_PATH)
        self.assistant_service = AssistantService(URL_ASSISTANT)
        self.prompt_manager = PromptManager()
        self.guadrail = Model(self.prompt_manager.get_prompt())

    def service_execute(self, query):
        intention = self.guadrail.invoke({"query": query})
        logging.info("Guadrail: '%s'", intention)
        if intention.strip().lower() == 'toxico':
            return "Lo siento no puedo ayudarte con esta pregunta."
        """
        intention = self.sr_router(query).name
        if intention is None:
            logging.debug("Intención no encontrada para el query: '%s'", query)
            return "Por favor Reformule su pregunta"
        """
        if intention == "chat_rag":
            endpoint = "/assistant/rag"
        elif intention == "analisis_pdf":
            endpoint = "/assistant/analyze-pdf"
        elif intention == "asesor_compras":
            endpoint = "/assistant/shopping-advisor"

        logging.info("Intención procesada: '%s', Endpoint seleccionado: '%s'", intention, endpoint)
        
        response = self.assistant_service.post_request(endpoint, {"query": query})    
        return response