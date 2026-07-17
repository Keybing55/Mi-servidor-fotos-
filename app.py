from fastapi import FastAPI, Request
from gradio_client import Client

app = FastAPI()
client = Client("https://kcai123-mi-servidor-fotos.hf.space/")

# Esto nos ayudará a ver los nombres reales de las funciones
print("Funciones disponibles en el Space:", client.view_api())

@app.api_route("/{path:path}", methods=["GET", "POST"])
async def catch_all(request: Request, path: str):
    data = await request.json() if request.method == "POST" else {}
    
    # Aquí cambiaremos '/predict' por el nombre correcto en cuanto veamos los logs
    result = client.predict(
        image=data.get("image"),
        prompt=data.get("prompt"),
        api_name="/procesar_foto" 
    )
    return {"resultado": result}
