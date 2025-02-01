import requests

class AssistantService:
    def __init__(self, base_url):
        #self.base_url = base_url
        self.base_url = "http://127.0.0.1:5000"

    def post_request(self, endpoint, data, headers=None):
        """Envía una solicitud POST a la API"""
        url = f"{self.base_url}{endpoint}"
        
        try:
            # Si no se proporcionan headers, se usan headers predeterminados
            if not headers:
                headers = {
                    'Content-Type': 'application/json'
                }
            
            # Realizar la solicitud POST
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
            # Captura cualquier error durante la solicitud
            return {
                'error': True,
                'message': str(e)
            }
