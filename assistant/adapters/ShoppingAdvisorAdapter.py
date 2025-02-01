from flask_restful import Resource

class ShoppingAdvisorAdapter(Resource):
    def post(self):
        return {"response": "hola desde shopping advisor"}