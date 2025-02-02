from langchain_community.utilities import SerpAPIWrapper
from langchain_core.tools import Tool
from langchain.agents import initialize_agent, AgentType

import os

from model.model import Model
from utils.PromptManager import PromptManager
from langchain_core.prompts import PromptTemplate

SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

prompt_manager = PromptManager()


class WebSearchAgent():
    def __init__(self):
        self.llm = Model()
        self.agent = self._init_agent()
        self.prompt_manager = PromptManager()  

        prompt_text = self.prompt_manager.get_prompt("web_search_prompt")

        self.prompt = PromptTemplate(
            input_variables=["query"],  
            template=prompt_text
        )

    def _init_agent(self):
        #Buscador gl: ubicacion(Ecuador) - hl:idioma (espanol) - num: numero maximo de documentos a retornar 
        search = SerpAPIWrapper(serpapi_api_key=SERPAPI_API_KEY, params={"gl": "ec", "hl": "es", "num": "10"})

        #Crear tool
        web_search_tool = Tool(
            name="google_search",
            description="Search Google for recent results.",
            func=search.results,
        )

        return initialize_agent(
            tools=[web_search_tool],
            llm=self.llm.get_llm(),
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            max_iterations=5,
            handle_parsing_errors=True,
        )

    def get_agent(self):
        return self.agent
    
    def invoke_agent(self, query):
        full_prompt = self.prompt.format_prompt(query=query).text
        return self.agent.invoke(full_prompt)