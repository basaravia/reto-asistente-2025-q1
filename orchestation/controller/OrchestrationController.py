import logging
import os
from model.model import Model
from utils.PromptManager import PromptManager
from service.AssistantService import AssistantService

logging.basicConfig(level=logging.DEBUG)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
FILE_PATH = os.path.join(BASE_DIR, "..", "utils", "data", "semantic_router.json")

ASSISTANT_HOST = os.getenv("ASSISTANT_HOST")

class OrchestrationController():
    def __init__(self):
        self.assistant_service = AssistantService(ASSISTANT_HOST)
        self.prompt_manager = PromptManager()
        self.guadrail = Model(self.prompt_manager.get_prompt())

    def service_execute(self, query, pdfbase64):
        intention = self.guadrail.invoke({"query": query})
        logging.info("Guadrail: '%s'", intention)

        if intention.strip().lower() == 'toxico':
            return "Lo siento no puedo ayudarte con esta pregunta."
        if intention == "chat_rag":
            endpoint = "/assistant/rag"
        elif intention == "analisis_pdf":
            endpoint = "/assistant/analyze-pdf"
        elif intention == "asesor_compras":
            endpoint = "/assistant/shopping-advisor"

        logging.info("Intención procesada: '%s', Endpoint seleccionado: '%s'", intention, endpoint)
        
        response = self.assistant_service.post_request(endpoint, query, pdfbase64)

        return response