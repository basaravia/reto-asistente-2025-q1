from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

import os

GEMINI_API_KEY = os.getenv("API_KEY_GEMINI")

if not GEMINI_API_KEY:
    raise ValueError("❌ ERROR: La clave API de Gemini no se ha cargado correctamente.")

class Model():
    def __init__(self):
        self.llm = self.__configurateModel()
        self.prompt = ""

    def __configurateModel(self):
        return ChatGoogleGenerativeAI(
            model="gemini-2.0-flash-exp",
            google_api_key=GEMINI_API_KEY,
            temperature=0.2,         
            top_p=0.8,
            top_k=40
        )

    def get_llm(self):
        return self.llm
    
    def set_prompt(self, prompt):
        self.prompt = PromptTemplate.from_template(prompt)

    def invoke(self, variables):
        full_prompt = self.prompt.invoke(variables)
        response = self.llm.invoke(full_prompt)
        return response.content