import os
from gtts import gTTS

class TTS():
    def convert_text_to_speech(self, text):
        try:
            # Crea el objeto de gTTS
            speech = gTTS(text=text, lang='es', slow=False)
            file_name = "response.mp3"
            file_path = os.path.join("temp", file_name)

            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            speech.save(file_path)
            return file_name
        except Exception as e:
            print(f"Error al convertir texto a voz: {e}")
            return None

