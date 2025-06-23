from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pymongo import MongoClient

# Create FastAPI app
app = FastAPI()

# Load static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Load Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["notes"]               
notes_collection = db["notes"]    


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


#  Route to insert a new note
@app.post("/add-note/")
async def add_note(note: dict):
    result = notes_collection.insert_one(note)
    return {"status": "success", "inserted_id": str(result.inserted_id)}


#  Route to fetch all notes
@app.get("/notes/")
async def get_notes():
    notes = list(notes_collection.find({}, {"_id": 0}))  # exclude Mongo's _id field
    return {"notes": notes}
