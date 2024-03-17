# from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
from typing import Any, Annotated
from chat import chatbot
import os
import uvicorn

# Directory to save uploaded files
UPLOAD_DIRECTORY = "upload"

# Create the upload directory if it doesn't exist
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)


origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000"
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/predict")
def predict(question: Annotated[str, Form()], files: list[UploadFile]) -> Any:
    question=str(question)
    paths=[]
    print(len(files))
    for f in files:
        file_path = os.path.join(UPLOAD_DIRECTORY, f.filename)
        with open(file_path, "wb") as buffer:
            buffer.write(f.read())
            paths.append(file_path)

    # result=chatbot(paths, question)
    result="ans"
    return {"result": result}

if __name__=="__main__":
    uvicorn.run(app, host="http://127.0.0.1", port=8000)