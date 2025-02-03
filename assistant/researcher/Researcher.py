from langchain_ollama import ChatOllama
from langchain_community.utilities import SerpAPIWrapper
import json
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from dotenv import load_dotenv
assert load_dotenv()
model = ChatOllama(model="deepseek-r1:8b", temperature=0.1, base_url="http://host.docker.internal:11434")
search = SerpAPIWrapper(params={"gl": "ec", "hl": "es", "num": "11"})
inputSystem = """
El usuario te enviará una lista de productos con sus respectivas urls, probablemente precios y demás.
Quiero que organices esta lista de jsons, en una tabla organizada con los productos más baratos primeros.
Además debe verse de la siguiente forma.
Nunca digas de donde obtuviste la informacion, pero siempre agrega una nota que nos indique que para verificar la informacion visitemos los links.
Id (orden 1,2,3,4,5...)| Nombre del producto | Tienda | link 
"""
prompt = ChatPromptTemplate.from_messages([
    ("system", inputSystem),
    ("user", "{user_input}")
])

class Researcher:
    def __init__(self, user_input: str):
        self.user_input = user_input
    def search(self):
        search = SerpAPIWrapper(params={"gl": "ec", "hl": "es", "num": "11"})
        respuesta = search.results(f"{self.user_input} PRECIOS MÁS ECONÓMICOS")
        respuesta = [
            {k: v for k, v in x.items() if k not in ["redirect_link", "displayed_link", "favicon","position"]}
            for x in respuesta["organic_results"]
        ]
        return json.dumps(respuesta)
    def research(self):
        chain = prompt | model | StrOutputParser()
        respuesta = chain.invoke({"user_input": self.search()}).split("</think>")[1]
        return respuesta
