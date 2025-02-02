from flask import request
from flask_restful import Resource

from controller.OrchestrationController import OrchestrationController


class OrchestrationAdapter(Resource):
    def __init__(self, orchestration_controller: OrchestrationController):
        self.orchestation_controller = orchestration_controller
        
    def post(self):
        query, pdfbase64 = self._getBody(request)
        response = self.orchestation_controller.service_execute(query, pdfbase64)

        return {"response": response}
    
    def _getBody(self, request):
        body = request.get_json()
        pdf_encode = body.get('pdf_encode', None)
        query = body.get('query', None)
        return query, pdf_encode
