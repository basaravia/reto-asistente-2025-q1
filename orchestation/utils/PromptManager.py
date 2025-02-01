import json
import os
# Obtener la ruta del directorio donde está este script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  

# Construir la ruta absoluta al archivo JSON
FILE_PATH = os.path.join(BASE_DIR, "data", "prompt.json")

class PromptManager:
    def __init__(self):
        self.file_path = os.path.abspath(FILE_PATH)
        self.prompt_data = self._load_prompt()
        print(f"Este archivo se encuentra en: {self.file_path}")

    def _load_prompt(self):
        """Carga el prompt desde un archivo JSON."""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error al cargar el prompt: {e}")
            return None
    
    def get_prompt(self):
        if self.prompt_data and "system_prompt" in self.prompt_data:
            return self.prompt_data["system_prompt"]
        return None