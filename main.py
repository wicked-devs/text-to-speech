from text_to_speech import save
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from starlette.background import BackgroundTask
import os

class Item(BaseModel):
    text: str
    language: str = "en"

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "hello world"}

@app.post("/speech/")
async def text_to_speech(item: Item):
    text = item.text
    language = item.language
    output_file = "speech.mp3"
    save(text, language, file=output_file)

    if os.path.exists(output_file):
        # Use BackgroundTask to delete the file after the response is sent
        def cleanup():
            os.remove(output_file)

        return FileResponse(
            path=output_file,
            media_type='audio/mpeg',
            filename=output_file,
            background=BackgroundTask(cleanup)
        )
    else:
        return {"message": "File not found"}
