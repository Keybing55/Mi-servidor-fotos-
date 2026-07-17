from fastapi import FastAPI, UploadFile, File, Form
from gradio_client import Client
import shutil
import os

app = FastAPI()

# Conecta a tu Space
client = Client("https://kcai123-mi-servidor-fotos.hf.space/")

@app.post("/procesar")
async def procesar(image: UploadFile = File(...), prompt: str = Form(...)):
    # Guardar imagen temporalmente
    with open(image.filename, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    
    # Enviar a Hugging Face
    result = client.predict(
        image=image.filename, 
        prompt=prompt, 
        api_name="/predict" 
    )
    
    # Limpiar archivo temporal
    os.remove(image.filename)
    
    return {"resultado": result}
