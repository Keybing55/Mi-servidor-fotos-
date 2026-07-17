from fastapi import FastAPI, Request
from gradio_client import Client

app = FastAPI()
client = Client("https://kcai123-mi-servidor-fotos.hf.space/")

# Esto captura cualquier ruta que tu app intente buscar
@app.api_route("/{path:path}", methods=["GET", "POST"])
async def catch_all(request: Request, path: str):
    # Obtiene los datos de la petición
    data = await request.json() if request.method == "POST" else {}
    
    # Redirige todo al endpoint /predict que espera Hugging Face
    result = client.predict(
        image=data.get("image"),
        prompt=data.get("prompt"),
        api_name="/predict"
    )
    return {"resultado": result}
