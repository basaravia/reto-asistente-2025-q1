from model.model import Model
from service.RagService import RagService
from utils.PromptManager import PromptManager


class RagController():
    def __init__(self):
        self.llm = Model()
        self.rag_service = RagService()
        prompt_manager = PromptManager()
        self.prompt = prompt_manager.get_prompt("rag_prompt")
        self._set_prompt()

    def _set_prompt(self):
        self.llm.set_prompt(self.prompt)

    def service_execute(self, query):
        context = self.rag_service.execute_rag(query)
        response = self.llm.invoke({
            "query": query,
            "context": context
        })

        return response
