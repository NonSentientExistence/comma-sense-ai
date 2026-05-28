from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse

from typing import Annotated

app = FastAPI()

@app.get("/health")
async def root():
    return {"status": "ok"}


@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<label for="file-upload" class="form-label">Select file:</label>
<input
    type="file"
    id="file-upload"
    name="file"
    accept=".csv"
    aria-describedby="file-help"
  />
<div id="file-help" class="form-text">Accepted formats: CSV</div>
<button type="submit">Upload File</button>
</form>
</body>
    """
    return HTMLResponse(content=content)


@app.post("/data/upload/")
async def upload_file(file: UploadFile):
   if not file.file.filename.endswith(".csv"):
       raise HTTPException(status_code=400, detail="Only CSV files allowed")
   
   contents = await file.read()