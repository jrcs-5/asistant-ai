from dotenv import load_dotenv
import os
import requests

class TVController():
    def __init__(self):
        self.psk = None
        self.ip = None
    
    
    def cargar(self):
        load_dotenv()
        self.psk = os.getenv("PSK_TV")
        self.ip = os.getenv("IP_TV")
        if not self.psk or not self.ip:
            raise ValueError("Datos para conexion con la tv no almacenados en env.")
        
    def _send_request(self, service, method, params=None):
        if not self.ip or not self.psk:
            raise ValueError("No se ha configurado la IP o el PSK.")
        url = f"http://{self.ip}/sony/{service}"
        headers = {"X-Auth-PSK": self.psk}
        payload = {
            "method": method,
            "version": "1.0",
            "id": 1,
            "params": [params] if params else []
        }
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
        
    
    def prender(self):
        self._send_request("system", "setPowerStatus", {"status": True})
        print("La TV ha sido encendida.")
        response = "Listo, ya prendí la televisión."
        return response
    
    def apagar(self):
        self._send_request("system", "setPowerStatus", {"status": False})
        print("La TV ha sido apagada.")
        response = "Listo, ya apagué la televisión."
        return response

    
    def prender_play(self):
        self._send_request("avContent", "setPlayContent", {"uri": "extInput:cec?type=player&port=2&logicalAddr=4"})
        print(f"Encendiendo play.")
        response  = "Listo, ya prendí la play station."
        return response
        
    def mutear(self):
        self._send_request("audio", "setAudioMute", {"status": True})
        print("Se muteó.")
        response = "Listo, ya muteé la televisión."
        return response
        
    def desmutear(self):
        self._send_request("audio", "setAudioMute", {"status": False})
        print("Se desmuteó.")
        response = "Listo, ya desmuteé la televisión"
        return response
        
        
    
        
        
        
    #Funciones de prueba
    def prueba_get_content(self):
        req = self._send_request("avContent", "getPlayingContentInfo")
        print(req)
        
    def prueba_hdmi_2(self):
        self._send_request("avContent", "setPlayContent", {"uri": "extInput:hdmi?port=2"})
        print(f"Abrir el puerto 2 para la play.")