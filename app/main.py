from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import HTMLResponse
import io
import pandas as pd
import numpy as np

from typing import Annotated

from app import data
from app.schemas import PromptBuilderInput, UserQuestionInput
from app.chain.pipeline import oraklet

app = FastAPI()

@app.get("/health")
async def root():
    return {"status": "ok"}


@app.get("/")
async def main():
    content = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>comma-sense-ai</title>
    <style>
        body { font-family: sans-serif; max-width: 700px; margin: 40px auto; padding: 0 20px; }
        section { border: 1px solid #ccc; border-radius: 8px; padding: 20px; margin-bottom: 20px; }
        h2 { margin-top: 0; }
        input, select, button, textarea { font-size: 1rem; padding: 6px; margin: 4px 0; }
        button { cursor: pointer; }
        #upload-status, #answer { margin-top: 12px; white-space: pre-wrap; }
        .muted { color: #666; }
        textarea { width: 100%; box-sizing: border-box; }
    </style>
</head>
<body>
    <h1>comma-sense-ai</h1>

    <section>
        <h2>1. Upload CSV</h2>
        <input type="file" id="file-upload" accept=".csv" />
        <select id="separator">
            <option value=",">Comma (,)</option>
            <option value=";">Semicolon (;)</option>
            <option value="\\t">Tab</option>
        </select>
        <button onclick="uploadFile()">Upload</button>
        <div id="upload-status" class="muted"></div>
    </section>

    <section>
        <h2>2. Ask a question</h2>
        <textarea id="question" rows="2" placeholder="e.g. Which game sold the most?"></textarea>
        <button onclick="askQuestion()">Ask</button>
        <div id="answer"></div>
    </section>

    <script>
        async function uploadFile() {
            const fileInput = document.getElementById("file-upload");
            const separator = document.getElementById("separator").value;
            const status = document.getElementById("upload-status");

            if (!fileInput.files.length) {
                status.textContent = "Please choose a CSV file first.";
                return;
            }

            const formData = new FormData();
            formData.append("file", fileInput.files[0]);
            formData.append("separator", separator);

            status.textContent = "Uploading...";
            try {
                const res = await fetch("/data/upload/", { method: "POST", body: formData });
                const data = await res.json();
                if (!res.ok) {
                    status.textContent = "Error: " + (data.detail || "upload failed");
                    return;
                }
                status.textContent = "Loaded " + data.rows + " rows. Columns: " + data.columns.join(", ");
            } catch (err) {
                status.textContent = "Error: " + err;
            }
        }

        async function askQuestion() {
            const question = document.getElementById("question").value;
            const answer = document.getElementById("answer");

            if (!question.trim()) {
                answer.textContent = "Please type a question.";
                return;
            }

            answer.textContent = "Thinking... (first question loads the model, may take a minute)";
            try {
                const res = await fetch("/ai/ask", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ question: question })
                });
                const data = await res.json();
                if (!res.ok) {
                    answer.textContent = "Error: " + (data.detail || "request failed");
                    return;
                }
                answer.textContent = data.answer;
            } catch (err) {
                answer.textContent = "Error: " + err;
            }
        }
    </script>
</body>
</html>
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
    try:
        data.current_df = pd.read_csv(io.BytesIO(contents), sep = separator)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not read CSV: {e}")
    
    if data.current_df.empty:
        raise HTTPException(status_code=400, detail="CSV contains no data")

    return {
        "rows": len(data.current_df),
        "columns": data.current_df.columns.tolist(),
        "dtypes": data.current_df.dtypes.astype(str).to_dict()
    }

@app.get("/data/stats")
async def data_stats():
    if data.current_df is None:
        raise HTTPException(status_code=404, detail="No CSV data has been uploaded")
    return data.current_df.describe().replace({np.nan: None}).to_dict()

@app.post("/ai/ask")
async def ask_question(input: UserQuestionInput):
    if data.current_df is None:
        raise HTTPException(status_code=400, detail="No CSV has been uploaded")
    
    stats = data.current_df.describe().fillna(0).to_dict()

    chain_input = PromptBuilderInput(
        question=input.question,
        stats=stats
    )

    result = oraklet.invoke(chain_input)
    return result