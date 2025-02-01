from semantic_router.layer import RouteLayer
import logging
logging.basicConfig(level=logging.DEBUG)


class OrchestrationController():
    def __init__(self):
        # Antes de la inicialización
        logging.debug("Inicializando semantic_router...")

        self.sr_router = RouteLayer.from_json("utils/semantic_router.json")

        # Después de la inicialización
        logging.debug("Semantic_router inicializado.")

    def service_execute(self, query):
        intention = self.sr_router(query).name
        if intention is None:
            intention = "Por favor Reformule su pregunta"
        return intention