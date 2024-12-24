from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from modules.transcriber import Transcriber
from modules.llm import LLM
from modules.tts import TTS
from modules.command_handler import CommandHandler
import traceback

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/temp", StaticFiles(directory="temp"), name="temp")

transcriber = Transcriber()
command_handler = CommandHandler()
llm = LLM()
tts = TTS()



@app.on_event("startup")
async def startup_event():
    print("Ejecutando tareas de inicio...")
    transcriber.load_model()





@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("recorder.html", {"request": request})


@app.post("/audio")
async def audio(audio: UploadFile = File(...)):
    if audio:
        file_path = f"temp/{audio.filename}"
        
        try:
            with open(file_path, "wb") as f:
                f.write(await audio.read())
                
                text = transcriber.get_transcribe(file_path)
                function_name, function_args, message = llm.process_functions(text)

                if function_name is not None:
                    function_response = command_handler.create_command(function_name, function_args)
                    response = llm.process_response(message, function_name, function_response)

                    message = response
                    try:
                        message = response.candidates[0].content.parts[0].text
                    except (IndexError, KeyError, AttributeError) as e:
                        print(f"Error al extraer el texto: {e}")
                        print("Error: 'response' no es válido:", response)
                        message = f"Error procesando la respuesta: {response}"
                        
            # Convertir texto a voz
            tts_file = tts.convert_text_to_speech(message)
            
            print("Fin de procesamiento de audio.")
            # Retornar respuesta
            return JSONResponse({"text": message, "file": tts_file})
        
        except Exception as e:
            print(f"Error procesando el archivo: {e}")
            traceback.print_exc()
            return JSONResponse({"error": f"Error procesando el archivo: {e}"}, status_code=500)

    return JSONResponse({"error": "No se recibió ningún archivo"}, status_code=400)

