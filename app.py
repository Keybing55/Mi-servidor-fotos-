from fastapi import FastAPI, Request
from gradio_client import Client

app = FastAPI()
client = Client("https://kcai123-mi-servidor-fotos.hf.space/")

@app.api_route("/{path:path}", methods=["GET", "POST"])
async def catch_all(request: Request, path: str):
    # Intentamos obtener los datos de forma flexible
    try:
        data = await request.form()
        print("Datos recibidos:", data) # Esto imprimirá lo que llega a los logs
        
        result = client.predict(
            image=data.get("image"),
            prompt=data.get("prompt"),
            api_name="/procesar_foto"
        )
        return {"resultado": result}
    except Exception as e:
        print("Error detallado:", str(e))
        return {"error": str(e)}
