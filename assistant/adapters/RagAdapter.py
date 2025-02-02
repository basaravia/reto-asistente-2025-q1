from flask import request
from flask_restful import Resource

from controller.RagController import RagController

class RagAdapter(Resource):
    def __init__(self):
        super().__init__()
        self.rag_controller = RagController()

    def post(self):
        query = self._getBody(request)
        response = self.rag_controller.service_execute(query)
        return {"assistant_response": response}    
    
    def _getBody(self, request):
        body = request.get_json()
        return body['query']
