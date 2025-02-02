from flask_restful import Resource
from flask import request

from controller.AnalyzePdfControler import AnalyzePdfController

class AnalyzePdfAdapter(Resource):
    def __init__(self):
        super().__init__()
        self.analyze_pdf_controller = AnalyzePdfController()

    def post(self):
        query, pdf64 = self._getBody(request)
        response = self.analyze_pdf_controller.service_execute(query, pdf64)
        return {"assistant_response": response}    
    
    def _getBody(self, request):
        body = request.get_json()
        return body['query'], body['pdf_encode']