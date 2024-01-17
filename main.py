from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
import pandas as pd
from io import BytesIO

app = FastAPI()

# HTML que se muestra
html_form = """
<form method="post" enctype="multipart/form-data" action="/uploadfile/">
    <label for="file">Subir CSV: </label>
    <input type="file" name="file" accept=".csv">
    <input type="submit">
</form>
"""

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    df = pd.read_csv(BytesIO(contents))
    return {"filename": file.filename, "rows": len(df)}

@app.get("/form/")
async def form_post():
    return HTMLResponse(content=html_form, status_code=200)
