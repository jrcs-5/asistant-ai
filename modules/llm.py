import google.generativeai as genai
import google.generativeai.protos as prot
import os
from dotenv import load_dotenv

class LLM():
    def __init__(self):
        load_dotenv()
        genai.configure(api_key = os.getenv("GENAI_API_KEY"))   

        get_weather_func = prot.FunctionDeclaration(
            name = "get_weather",
            description = "Obtener el clima actual",
            parameters = prot.Schema(
                type = prot.Type.OBJECT,
                properties = {
                    "location": prot.Schema(
                        type = prot.Type.STRING,
                        description = "La ubicación, debe ser una ciudad"
                    )
                }
            )
        )
        send_email_func = prot.FunctionDeclaration(
            name = "send_email",
            description = "Enviar un correo",
            parameters = prot.Schema(
                type = prot.Type.OBJECT,
                properties = {
                    "recipient": prot.Schema(
                        type = prot.Type.STRING,
                        description = "El nombre de la persona que recibirá el correo electrónico"
                    ),
                    "subject": prot.Schema(
                        type = prot.Type.STRING,
                        description = "El asunto del correo"
                    ),
                    "body": prot.Schema(
                        type = prot.Type.STRING,
                        description = "El texto del cuerpo del correo"
                    )
                },
                required = ["recipient", "body"]
            )
        )
        open_chrome_func = prot.FunctionDeclaration(
            name = "open_chrome",
            description = "Abrir el explorador Chrome en un sitio específico",
            parameters = prot.Schema(
                type = prot.Type.OBJECT,
                properties = {
                    "website": prot.Schema(
                        type = prot.Type.STRING,
                        description = "El sitio al cual se desea ir"
                    )
                }
            )
        )
        get_time_func = prot.FunctionDeclaration(
            name = "get_time",
            description = "Obtener la hora actual",
            parameters = prot.Schema(
                type = prot.Type.OBJECT,
                properties = {
                    "location": prot.Schema(
                        type = prot.Type.STRING,
                        description = "La ubicación, debe ser una ciudad o un país"
                    )
                }
            )
        )     
        
        control_television_func = prot.FunctionDeclaration(
            name = "control_television",
            description = "Ejecutar una accion en la television que se encuentre entre las siguientes funcionalidades: prender la tv(prender), apagar la tv(apagar), prender el play station o jugar fifa, god of war o rocket league(prender_play), mutear la tv(mutear), desmutear la tv(desmutear)]",
            parameters = prot.Schema(
                type = prot.Type.OBJECT,
                properties = {
                    "action": prot.Schema(
                        type = prot.Type.STRING,
                        description = "La accion debe ser obligatoriamente solo una de las siguientes acciones permitidas: prender, apagar, prender_play, mutear, desmutear. Por ejemplo:prender"
                    )
                },
                required = ["action"]
            )
        )
        my_tools = [get_weather_func, send_email_func, open_chrome_func, get_time_func, 
                    control_television_func]
        
        self.model = genai.GenerativeModel(
            'gemini-1.5-flash-latest',
            generation_config = genai.GenerationConfig(
                temperature = 0.9,
            ),
            system_instruction = ["Eres un asistente virtual."],
            tools = my_tools
        )
        self.chat = self.model.start_chat(enable_automatic_function_calling=True)

    def process_functions(self, prompt):
        response = self.chat.send_message(prompt) #candidate_count=1
        message= response.candidates[0].content.parts[0].text
        if len(response.candidates[0].content.parts) > 1:
            if hasattr(response.candidates[0].content.parts[1], 'function_call'):
                function_call = response.candidates[0].content.parts[1].function_call
                function_name = function_call.name
                function_args = {key : value for key, value in function_call.args.items()}
                return function_name, function_args, message
        return None, None, message
    
    def process_response(self, message, function_name, function_response):
        response = self.chat.send_message(
            prot.Content(
                role = "model",
                parts = [prot.Part(
                    text = message,
                    function_response = prot.FunctionResponse(
                        name = function_name,
                        response = {'result' : function_response}
                    )
                )]
            )
        )
        return response