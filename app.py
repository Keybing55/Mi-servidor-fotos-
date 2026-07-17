from fastapi import FastAPI, UploadFile, File, Form
from gradio_client import Client
import shutil
import os

app = FastAPI()

client = Client("https://kcai123-mi-servidor-fotos.hf.space/")

# Ahora cambiamos la ruta a "/" (la raíz)
@app.post("/") 
async def procesar(image: UploadFile = File(...), prompt: str = Form(...)):
    with open(image.filename, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)
    
    result = client.predict(
        image=image.filename, 
        prompt=prompt, 
        api_name="/predict" 
    )
    
    os.remove(image.filename)
    
    return {"resultado": result}
