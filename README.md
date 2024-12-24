# 📡 **Asistente Virtual de Python**
Este proyecto es un asistente virtual basado en Python que utiliza Gemini y la API de televisores Sony Bravia para controlar dispositivos y realizar tareas personalizables.


---


## 📦 **Instalación y Configuración**  
### **Requisitos previos:**  
- Python 3.11 o superior  
- Git  

### **Pasos para configurar el proyecto:**  
- Clonar el repositorio
- Opcional: Crea un ambiente virtual
- Instala las dependencias ejecutando 
	- ```  pip install -r requirements.txt ```
- Crea un archivo `.env` en la raíz del proyecto y define las siguientes variables:
```plaintext
    GENAI_API_KEY=tu_clave_genai
    PSK_TV=tu_clave_psk_tv
    IP_TV=la_direccion_ip_de_tu_tv
    TIME_API_KEY=tu_clave_api_para_tiempo
```

---

## 🚀 **Ejecución del Servidor**
- Para iniciar el servidor de FastAPI, ejecuta el siguiente comando:
    - ``` uvicorn main:app --reload```
    - En tu navegador ve a http://127.0.0.1:8000
    - Puedes ver la documentación en http://127.0.0.1:8000/docs



---

## 🛠️ **Personalización y Extensiones**
### **Archivos clave para personalización:**
- **`command_handler.py`**: Agrega aquí las funcionalidades adicionales que quieras implementar.
- **`llm.py`**: En la sección `system_instruction`, define las directivas personalizadas para el modelo Gemini.
- **`tv_controller.py`**: Modifica este archivo para adaptarlo a la API específica de tu televisor.

---

## ⚠️ **Notas**
- **No todas las funcionalidades están completamente implementadas.** Algunas requieren configuraciones adicionales.
- Creditos de las imágenes `record.png` y `stop.png` a sus respectivos autores.

---

## 🌟 **Contribuciones**
¡Las contribuciones son bienvenidas! Si tienes ideas o mejoras, no dudes en enviar un pull request o abrir un issue.



