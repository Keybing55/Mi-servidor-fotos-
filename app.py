from fastapi import FastAPI, Request
from gradio_client import Client
import shutil
import os

app = FastAPI()
client = Client("https://kcai123-mi-servidor-fotos.hf.space/")

@app.api_route("/{path:path}", methods=["GET", "POST"])
async def catch_all(request: Request, path: str):
    temp_file_path = None
    try:
        form = await request.form()
        print("Datos recibidos:", form)
        
        # Extraer el archivo de imagen recibido del móvil
        image_file = form.get("image")
        prompt = form.get("prompt", "")
        
        if image_file:
            # Guardar el UploadFile temporalmente en el disco de Render
            temp_file_path = f"temp_{image_file.filename}"
            with open(temp_file_path, "wb") as buffer:
                shutil.copyfileobj(image_file.file, buffer)
        else:
            return {"error": "No se encontró ninguna imagen en la petición"}

        # Llamar a Hugging Face usando la ruta del archivo temporal (un string válido)
        result = client.predict(
            image=temp_file_path,
            prompt=prompt,
            api_name="/procesar_foto"
        )
        
        # Limpiar archivo temporal
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            
        return {"resultado": result}
        
    except Exception as e:
        # Asegurarse de limpiar si ocurre un error
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            
        print("Error detallado:", str(e))
        return {"error": str(e)}
