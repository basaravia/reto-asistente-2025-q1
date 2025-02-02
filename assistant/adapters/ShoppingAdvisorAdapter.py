from flask_restful import Resource
from flask import request

from controller.ShoppingAdvisorCotroller import ShoppingAdvisorController

class ShoppingAdvisorAdapter(Resource):
    def __init__(self):
        super().__init__()
        self.shopping_advisor_controller = ShoppingAdvisorController()

    def post(self):
        data = self._getBody(request)
        response = self.shopping_advisor_controller.service_execute(data['query'])
        return response
    
    def _getBody(self, request):
        body = request.get_json()
        return body