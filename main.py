import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pymongo import MongoClient

app = FastAPI(title="My Test Backend")

# 1. CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. MongoDB Setup
MONGO_URL = os.environ.get("MONGO_URL")
collection = None
try:
    if MONGO_URL:
        client = MongoClient(MONGO_URL)
        db = client["myDatabase"]
        collection = db["test_collection"]
        print("MongoDB Connected Successfully! 🎉")
except Exception as e:
    print(f"Database connection error: {e}")


# 3. 🌐 मुख्य रूट: यह गिटहब पर मौजूद index.html फ़ाइल को लोड करके स्क्रीन पर दिखाएगा
@app.get("/", response_class=HTMLResponse)
def home():
    try:
        # यह आपके गिटहब प्रोजेक्ट की index.html फ़ाइल को पढ़ेगा
        with open("index.html", "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        return f"<h1>index.html फ़ाइल लोड करने में एरर आया: {str(e)}</h1>"


# 4. बाकी सारे पुराने रूट्स
@app.get("/hello")
def hello():
    return {"message": "Hello from Railway! 🚀"}


@app.get("/user/{name}")
def user(name: str):
    return {"name": name, "message": f"Hello {name}!"}


@app.get("/add")
def add(a: int, b: int):
    return {"a": a, "b": b, "result": a + b}


@app.get("/get-db-data")
def get_db_data():
    if collection is None:
        return {"status": "error", "message": "डेटाबेस कनेक्टेड नहीं है।"}
    try:
        items = list(collection.find({}, {"_id": 0}))
        return {"status": "success", "data": items}
    except Exception as e:
        return {"status": "error", "message": str(e)}
