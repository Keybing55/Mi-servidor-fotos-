from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from gradio_client import Client
import shutil
import os

app = FastAPI()
client = Client("https://kcai123-mi-servidor-fotos.hf.space/")

@app.api_route("/{path:path}", methods=["GET", "POST"])
async def catch_all(request: Request, path: str):
    temp_file_path = None
    output_path = None
    try:
        form = await request.form()
        image_file = form.get("image")
        prompt = form.get("prompt", "")
        
        if image_file:
            temp_file_path = f"temp_{image_file.filename}"
            with open(temp_file_path, "wb") as buffer:
                shutil.copyfileobj(image_file.file, buffer)
        else:
            return JSONResponse(status_code=400, content={"error": "No se encontró ninguna imagen"})

        # Llamar a Hugging Face
        output_path = client.predict(
            image=temp_file_path,
            prompt=prompt,
            api_name="/procesar_foto"
        )
        
        # El cliente de Gradio devuelve la ruta del archivo de salida. 
        # Vamos a leer ese archivo en bytes para devolvérselo directamente al móvil.
        if output_path and os.path.exists(output_path):
            with open(output_path, "rb") as img_file:
                image_bytes = img_file.read()
            
            # Limpiar archivos temporales
            os.remove(temp_file_path)
            
            # Devolver la imagen pura al móvil con el tipo correcto
            return Response(content=image_bytes, media_type="image/png")
        else:
            return JSONResponse(status_code=500, content={"error": "La IA no devolvió ninguna imagen"})
            
    except Exception as e:
        if temp_file_path and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        print("Error detallado:", str(e))
        return JSONResponse(status_code=500, content={"error": str(e)})
