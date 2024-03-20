from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Any, Annotated
from chat import chatbot # Assuming chatbot is a custom module you've created
import os
import uvicorn

# Directory to save uploaded files
UPLOAD_DIRECTORY = "upload"

# Create the upload directory if it doesn't exist
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

# Define allowed origins for CORS
origins = [
    "*",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000"
]

# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware to allow cross-origin requests from specified origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

# Define endpoint for prediction
@app.post("/predict")
async def predict(question: Annotated[str, Form()], files: list[UploadFile]) -> Any:
    # Convert question to string
    question=str(question)

    # List to store file paths
    paths=[]
    for f in files:
        file_path = os.path.join(UPLOAD_DIRECTORY, f.filename)

        # Write the file content to disk
        with open(file_path, "wb") as buffer:
            buffer.write(await f.read())
            paths.append(file_path)

    # Call chatbot function with uploaded file paths and question
    result=chatbot(paths, question)
    return {"result": result}


# Run the FastAPI app using uvicorn server
if __name__=="__main__":
    uvicorn.run(app, host="http://127.0.0.1", port=8000)