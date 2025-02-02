import json
import os
# Obtener la ruta del directorio donde está este script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  

# Construir la ruta absoluta al archivo JSON
FILE_PATH = os.path.join(BASE_DIR, "data", "prompts.json")

class PromptManager:
    def __init__(self):
        self.file_path = os.path.abspath(FILE_PATH)
        self.prompt_data = self._load_prompt()

    def _load_prompt(self):
        """Carga el prompt desde un archivo JSON."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error al cargar el prompt: {e}")
            return None
    
    def get_prompt(self, prompt_name=None):
        if self.prompt_data and prompt_name in self.prompt_data:
            return self.prompt_data[prompt_name]
        return None