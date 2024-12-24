import whisper
import os

class Transcriber():
    def load_model(self):
        self.model = whisper.load_model('base')

    def get_transcribe(self, path):
        try:
            # Realizar la transcripción
            result = self.model.transcribe(path, language='es', verbose=True)

            return result.get('text', '')
        except Exception as e:
            print(f"Error al transcribir el archivo: {e}")
            return ''