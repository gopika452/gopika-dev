from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
import os

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    return {"filename": file.filename, "size": len(content)}

@app.post("/message")
async def collect_message(message: str = Form(...)):
    return {"message_received": message, "response": f"You said: '{message}'"}

@app.delete("/delete")
async def delete_file(filename: str = Form(...)):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return {"message": f"File '{filename}' deleted successfully"}
    else:
        return JSONResponse(status_code=404, content={"error": "File not found"})







