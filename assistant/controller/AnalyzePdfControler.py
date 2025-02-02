from utils.ProcessPDF import ProcessPDF
from model.model import Model
from utils.PromptManager import PromptManager

prompt_manager = PromptManager()

class AnalyzePdfController():
    def __init__(self):
        self.llm = Model()
        self.process_pdf = ProcessPDF()
        self.prompt = prompt_manager.get_prompt("financial_assistant_prompt")
        self._set_prompt()

    def _set_prompt(self):
        self.llm.set_prompt(self.prompt)

    def service_execute(self, query, pdf_base64):
        context = self.process_pdf.get_pdf_info(pdf_base64)
        print("CONTEXTO RECUPERADO: ", context)
        response = self.llm.invoke({
            "query": query,
            "context": context
        })

        return response
