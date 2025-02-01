from flask import request
from flask_restful import Resource

from controller.OrchestrationController import OrchestrationController


class OrchestrationAdapter(Resource):
    def __init__(self, orchestration_controller: OrchestrationController):
        self.orchestation_controller = orchestration_controller
        
    def post(self):
        data = request.get_json()
        query = data.get("query", None)
        response = self.orchestation_controller.service_execute(query)
        return {"response": response}