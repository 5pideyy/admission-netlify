from pymongo import MongoClient
from fastapi import FastAPI, HTTPException,Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

try:
    client = MongoClient("mongodb+srv://admin:K4lwF9358J6Mp4gC@cluster0.1wgqgg8.mongodb.net/?retryWrites=true&w=majority")
    db = client["admission_db"]
    collection = db["admission_form"]
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    raise SystemExit(1)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # "*" allows requests from any origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)
templates = Jinja2Templates(directory="frontend")


class AdmissionForm(BaseModel):
    name: str
    dob: str
    gender: str
    address: str
    email: str
    phone: str
    school: str
    mark: str
    graduationYear: str
    comments: str


@app.post("/submit_admission/")
async def submit_admission(form: dict):
    try:
        # Convert form data to Pydantic model
        admission_form = AdmissionForm(**form)
        # Insert the form data into the MongoDB database
        result = collection.insert_one(admission_form.dict())
        if result.acknowledged:
            return {"message": "Admission form submitted successfully"}
        else:
            raise HTTPException(status_code=500, detail="Error submitting the form")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)