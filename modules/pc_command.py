from subprocess import Popen
#Clase para ejecutar comandos en la PC
#De momento esta en duro, funciona para Windows
class PcCommand():
    def __init__(self):
        pass
    
    def open_chrome(self, website): #Open chorme
        website = "" if website is None else website
        try:
            Popen(["C:/Program Files/Google/Chrome/Application/chrome.exe", website])
            response = "Listo, ya abrí Chrome en el sitio " + website
        except Exception as e:
            Popen(["C:/Program Files/Google/Chrome/Application/chrome.exe"])
            response = f"Error al intentar abrir el sitio: {str(e)}"
        return response
        
    def send_email(self, recipient, subject, body):
        response = "Listo, se ha enviado el correo hacia " + recipient + "diciendo: " + body
        return response
        
    def get_time(self, location):
        
        
        
        response = "La hora en " + location + " es: 8pm"
        return response