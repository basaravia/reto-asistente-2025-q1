from flask_restful import Resource

class AnalyzePdfAdapter(Resource):
    def post(self):
        return {"response": "hola desde pdf adapter"}