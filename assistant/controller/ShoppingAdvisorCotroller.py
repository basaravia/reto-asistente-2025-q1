import json

from utils.WebSearchAgent import WebSearchAgent


class ShoppingAdvisorController():
    def __init__(self):
        self.web_search_agent = WebSearchAgent()
        pass

    def service_execute(self, query):
        agent_response = self.web_search_agent.invoke_agent(query)
        return self._json_parser_response(agent_response)
    
    def _json_parser_response(self, results):
        response = results['output'].strip("```json").strip("```").strip()

        return json.loads(response)