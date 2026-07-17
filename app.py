from fastapi import FastAPI, Request
from gradio_client import Client

app = FastAPI()
client = Client("https://kcai123-mi-servidor-fotos.hf.space/")

@app.api_route("/{path:path}", methods=["GET", "POST"])
async def catch_all(request: Request, path: str):
    # En lugar de forzar JSON, tomamos los datos de forma más flexible
    form_data = await request.form()
    
    # Enviamos los datos al Space
    result = client.predict(
        image=form_data.get("image"),
        prompt=form_data.get("prompt"),
        api_name="/procesar_foto"
    )
    return {"resultado": result}
