from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph
from typing import Dict, TypedDict
from langchain_core.output_parsers import StrOutputParser

class GraphState(TypedDict):
    input: str
    is_valid: bool
    is_toxic: bool
    refined_query: str
    context: str
    final_output: str

llm = ChatOllama(model="deepseek-r1:8b")
def call_model(system: str, dictionary:dict)->str:
    output_parser = StrOutputParser()
    prompt = ChatPromptTemplate.from_messages([
        ("system", system),
        ("user", "{user_input}")
    ])
    chain = prompt | llm | output_parser
    return chain.invoke(dictionary).split("</think>")[1].strip()
# Nodo 1: Guardrail -> Filtra temas bancarios y monetarios
def guardrail(state: GraphState) -> Dict:
    query = state["input"]
    inTopic = call_model("""Eres un modelo capaz de identificar si existen respuestas dentro de un tópico. Este Tópico se refiere a temas bancarios y monetarios
                 por lo que quiero que me digas si este query forma parte del este topico o no, Unicamente debes responder con SI o NO sin entregar ninguna explicación extra
                 evalua: cantidad de crédito disponible""",{"user_input": query})
    if "si" in inTopic.lower():
        return {"is_valid": True} 
    else:
        return {"is_valid": False, "final_output": "❌ Consulta rechazada: No es un tema bancario o monetario."}  # Termina en "end"

# Nodo 2: Toxicity -> Evalúa si el mensaje es tóxico
def toxicity(state: GraphState) -> Dict:
    query = state["input"]
    tox = call_model("""eres un modelo que verifica si existe toxicidad en un mensaje, es decir malas palabras, malas intenciones, o desagrado y desprestigio
en caso de que en la entrada del encuentres algo de lo mencionado anteriormente responde SI o en caso de no encontrar nada fuera de lo común responde NO. No entregues ningun contexto extra unicamente SI o NO.""",{"user_input": query})
    if "si" in tox.lower():
        return {"is_toxic": True, "final_output": "❌ Consulta rechazada: Contiene lenguaje inapropiado."}  # Termina en "end"
    else:
        return {"is_toxic": False}  # Sigue al nodo "rewriter"

# Nodo 3: Rewriter -> Reescribe la consulta para mejorar la estructura
def rewriter(state: GraphState) -> Dict:
    query = state["input"]
    refined_query =  call_model("""Mejora la estructura de la consulta del usuario consulta sin cambiar su significado con el objetivo de que funcione mejor en un sistema RAG.
                                No quiero ningun contexto extra solo entrega directamente el resultado de la mejora""",{"user_input": query})
    return {"refined_query": refined_query}

# Función RAG Dummy (Devuelve contexto fijo)
def rag_dummy(query: str) -> str:
    return "la tasa de interés es del 200%"

# Nodo 4: RAG -> Usa la función dummy para recuperar contexto
def rag_node(state: GraphState) -> Dict:
    refined_query = state["refined_query"]
    context = rag_dummy(refined_query)
    response = call_model("""En base a este contexto:<contexto>{contexto}</contexto> quiero que respondas de manera formal y directa al usuario sobre su duda, en caso de no ser posible debes responder que no tienes suficiente información. sin ningun texto extra es decir sin introduccion, presentación o despedida, Recuerda siempre escribir tu respuesta en español""",
                          {"user_input": query,"contexto":context})
    return {"context": context, "final_output": response}

# Nodo Final: Verifica el idioma de la respuesta y la traduce si es necesario
def end_node(state: GraphState) -> Dict:
    final_answer = state.get("final_output", "Error: No se generó una respuesta.")
    return {"final_output": final_answer}

# Crear el grafo con LangGraph
workflow = StateGraph(GraphState)

# Agregar nodos
workflow.add_node("guardrail", guardrail)
workflow.add_node("toxicity", toxicity)
workflow.add_node("rewriter", rewriter)
workflow.add_node("rag", rag_node)
workflow.add_node("end", end_node)

# Definir conexiones entre nodos
workflow.add_edge("guardrail", "toxicity")
workflow.add_edge("toxicity", "rewriter")
workflow.add_edge("rewriter", "rag")
workflow.add_edge("rag", "end")

# Función condicional para Guardrail
def guardrail_condition(state):
    if state.get("is_valid"):
        return "toxicity"
    else:
        return "end"

# Función condicional para Toxicity
def toxicity_condition(state):
    if state.get("is_toxic"):
        return "end"
    else:
        return "rewriter"

# Agregar transiciones condicionales
workflow.add_conditional_edges("guardrail", guardrail_condition)
workflow.add_conditional_edges("toxicity", toxicity_condition)

# Definir el nodo inicial
workflow.set_entry_point("guardrail")

# Compilar el grafo
app = workflow.compile()

# Ejecutar el flujo con una consulta válida
query = {"input": "¿Cuáles son las tasas de interés actuales en los bancos?"}
response = app.invoke(query)
print(response.get("final_output", "Error: No se generó respuesta."))

# # Prueba con una consulta no válida (fuera del tema)
# query = {"input": "¿Cuál es la mejor receta para hacer pizza?"}
# response = app.invoke(query)
# print(response.get("final_output", "Error: No se generó respuesta."))

# # Prueba con una consulta tóxica
# query = {"input": "Malditos bancos siempre roban el dinero"}
# response = app.invoke(query)
# print(response.get("final_output", "Error: No se generó respuesta."))
