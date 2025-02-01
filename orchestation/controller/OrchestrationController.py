from semantic_router.layer import RouteLayer
import logging

from service.AssistantService import AssistantService

logging.basicConfig(level=logging.DEBUG)

class OrchestrationController():
    def __init__(self):

        self.sr_router = RouteLayer.from_json("utils/semantic_router.json")
        self.assistant_service = AssistantService("http://127.0.0.1:5000")

    def service_execute(self, query):
        intention = self.sr_router(query).name
        if intention is None:
            return "Por favor Reformule su pregunta"
        if intention == "chat_rag":
            endpoint = "/assistant/rag"
        elif intention == "analisis_pdf":
            endpoint = "/assistant/analyze-pdf"
        elif intention == "asesor_compras":
            endpoint = "/assistant/shopping-advisor"

        response = self.assistant_service.post_request(endpoint)    
        return response