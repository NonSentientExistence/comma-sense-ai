from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import HTMLResponse
import io
import pandas as pd
import numpy as np

from typing import Annotated

from app import data

app = FastAPI()

@app.get("/health")
async def root():
    return {"status": "ok"}


@app.get("/")
async def main():
    content = """
<body>
<form action="/data/upload/" enctype="multipart/form-data" method="post">
<label for="file-upload" class="form-label">Select file:</label>
<input
    type="file"
    id="file-upload"
    name="file"
    accept=".csv"
    aria-describedby="file-help"
/>
<div id="file-help" class="form-text">Accepted formats: CSV</div>
<select name="separator" id="separator">
    <option value=",">Comma (,)</option>
    <option value=";">Semicolon (;)</option>
    <option value="\t">Tab</option>
</select>
<button type="submit">Upload File</button>
</form>

</body>
    """
    return HTMLResponse(content=content)


@app.post("/data/upload/")
async def upload_file(
    file: UploadFile,
    separator: str = Form(default=",")
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files allowed")

    contents = await file.read()
    data.current_df = pd.read_csv(io.BytesIO(contents), sep = separator)

    return {
        "rows": len(data.current_df),
        "columns": data.current_df.columns.tolist()
    }

@app.get("/data/stats")
async def data_stats():
    if data.current_df is None:
        raise HTTPException(status_code=404, detail="No CSV data has been uploaded")
    return data.current_df.describe().replace({np.nan: None}).to_dict()
