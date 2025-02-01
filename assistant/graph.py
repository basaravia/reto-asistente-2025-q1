from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph
from typing import Dict, TypedDict
from langchain_core.output_parsers import StrOutputParser
from Weaviate import get_context

class GraphState(TypedDict):
    input: str
    is_valid: bool
    is_toxic: bool
    refined_query: str
    context: str
    final_output: str
    pdf: str
    num_pag: str

class GraphWorkflow:
    def __init__(self):
        self.llm = ChatOllama(model="deepseek-r1:8b", base_url="http://host.docker.internal:11434")
        self.workflow = StateGraph(GraphState)
        self._setup_workflow()

    def call_model(self, system: str, dictionary: dict) -> str:
        output_parser = StrOutputParser()
        prompt = ChatPromptTemplate.from_messages([
            ("system", system),
            ("user", "{user_input}")
        ])
        chain = prompt | self.llm | output_parser
        return chain.invoke(dictionary).split("</think>")[1].strip()

    def guardrail(self, state: GraphState) -> Dict:
        query = state["input"]
        inTopic = self.call_model("""Eres un modelo capaz de identificar si existen respuestas dentro de un tópico. Este Tópico se refiere a temas bancarios y monetarios
                     por lo que quiero que me digas si este query forma parte del este topico o no, Unicamente debes responder con SI o NO sin entregar ninguna explicación extra
                     evalua el user_input""", {"user_input": query})
        if "si" in inTopic.lower():
            return {"is_valid": True}
        else:
            return {"is_valid": False, "final_output": "Consulta rechazada: No es un tema bancario o monetario."}

    def toxicity(self, state: GraphState) -> Dict:
        query = state["input"]
        tox = self.call_model("""Eres un modelo que verifica si existe toxicidad en un mensaje, es decir malas palabras, malas intenciones, o desagrado y desprestigio
        en caso de que en la entrada del encuentres algo de lo mencionado anteriormente responde SI o en caso de no encontrar nada fuera de lo común responde NO. No entregues ningun contexto extra unicamente SI o NO.""", {"user_input": query})
        if "si" in tox.lower():
            return {"is_toxic": True, "final_output": "Consulta rechazada: Contiene lenguaje inapropiado."}
        else:
            return {"is_toxic": False}

    def rewriter(self, state: GraphState) -> Dict:
        query = state["input"]
        refined_query = self.call_model("""Mejora la estructura de la consulta del usuario consulta sin cambiar su significado con el objetivo de que funcione mejor en un sistema RAG.
                                    No quiero ningun contexto extra. solo entrega directamente el resultado de la mejora en una sola linea es decir sin saltos de linea. Recuerda no dar ninguna introduccion ni nada más que la respuesta""", {"user_input": query})
        return {"refined_query": refined_query.replace("\n", " ")}

    def rag_node(self, state: GraphState) -> Dict:
        refined_query = state["refined_query"]
        context,pdf,numpag = get_context(refined_query)
        response = self.call_model("""En base a este contexto:<contexto>{contexto}</contexto> quiero que respondas de manera formal y directa al usuario sobre su duda, en caso de no ser posible debes responder que no tienes suficiente información. sin ningun texto extra es decir sin introduccion, presentación o despedida, Recuerda siempre escribir tu respuesta en español""",
                              {"user_input": refined_query, "contexto": context})
        return {"context": context, "final_output": response, "pdf": pdf, "num_pag": int(numpag)}

    def end_node(self, state: GraphState) -> Dict:
        final_answer = state.get("final_output", "Error: No se generó una respuesta.")
        
        num_pag = str(state.get("num_pag", 0))
        pdf = state.get("pdf", "Sin PDF")

        extra_info = f" Página: {num_pag} PDF: {pdf}" if (pdf != "Sin PDF" and "No se generó" not in final_answer) else ""

        return {"final_output": final_answer + extra_info}
    def guardrail_condition(self, state):
        if state.get("is_valid"):
            return "toxicity"
        else:
            return "end"

    def toxicity_condition(self, state):
        if state.get("is_toxic"):
            return "end"
        else:
            return "rewriter"

    def _setup_workflow(self):
        self.workflow.add_node("guardrail", self.guardrail)
        self.workflow.add_node("toxicity", self.toxicity)
        self.workflow.add_node("rewriter", self.rewriter)
        self.workflow.add_node("rag", self.rag_node)
        self.workflow.add_node("end", self.end_node)

        self.workflow.add_edge("guardrail", "toxicity")
        self.workflow.add_edge("toxicity", "rewriter")
        self.workflow.add_edge("rewriter", "rag")
        self.workflow.add_edge("rag", "end")

        self.workflow.add_conditional_edges("guardrail", self.guardrail_condition)
        self.workflow.add_conditional_edges("toxicity", self.toxicity_condition)

        self.workflow.set_entry_point("guardrail")
        self.app = self.workflow.compile()

    def invoke(self, query: Dict) -> str:
        response = self.app.invoke(query)
        return response.get("final_output", "Error: No se generó respuesta.")

# if __name__ == "__main__":
#     graph_workflow = GraphWorkflow()
#     query = {"input": "¿Cuáles son las tasas de interés actuales en los bancos?"}
#     response = graph_workflow.invoke(query)
#     print(response)