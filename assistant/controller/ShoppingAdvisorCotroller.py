import json

from utils.WebSearchAgent import WebSearchAgent


class ShoppingAdvisorController():
    def __init__(self):
        self.web_search_agent = WebSearchAgent()

    def service_execute(self, query):
        agent_response = self.web_search_agent.invoke_agent(query)
        return agent_response['output']
    