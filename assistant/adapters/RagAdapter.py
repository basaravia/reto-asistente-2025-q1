from flask_restful import Resource

class RagAdapter(Resource):
    def post(self):
        return {"response": "hola desde RAG"}