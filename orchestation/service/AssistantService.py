import requests

class AssistantService:
    def __init__(self, base_url):
        self.base_url = base_url

    def post_request(self, endpoint, data):
        """Envía una solicitud POST a la API"""
        url = f"{self.base_url}{endpoint}"
        headers = {"Content-Type": "application/json"}
        try:
            response = requests.post(url, json=data, headers=headers)
            
            # Verificar si la solicitud fue exitosa
            if response.status_code == 200:
                return response.json()  # Si la respuesta es JSON
            else:
                return {
                    'error': True,
                    'status_code': response.status_code,
                    'message': response.text
                }

        except requests.exceptions.RequestException as e:
            return {
                'error': True,
                'message': str(e)
            }
