import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient

app = FastAPI(title="My Test Backend")

# 1. CORS Setup (ताकि आपका फ्रंटएंड इस बैकएंड से डेटा ले सके)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # सभी फ्रंटएंड ऐप्स (लोकल या लाइव) को अनुमति देने के लिए
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST आदि सभी रिक्वेस्ट के लिए
    allow_headers=["*"],
)

# 2. MongoDB Setup (रेलवे के Variables से कनेक्शन उठाएगा)
MONGO_URL = os.environ.get("MONGO_URL")
try:
    if MONGO_URL:
        client = MongoClient(MONGO_URL)
        db = client["myDatabase"]  # आपके डेटाबेस का नाम
        collection = db["test_collection"]  # टेबल का नाम
        print("MongoDB Connected Successfully! 🎉")
    else:
        print("⚠️ MONGO_URL variable not found!")
except Exception as e:
    print(f"Database connection error: {e}")


# --- आपके पुराने वाले सारे रूट्स (Routes) यहाँ हैं ---

@app.get("/")
def home():
    return {
        "message": "Backend successfully deployed!",
        "status": "online"
    }


@app.get("/hello")
def hello():
    return {
        "message": "Hello from Render 🚀"  # या रेलवे :)
    }


@app.get("/user/{name}")
def user(name: str):
    return {
        "name": name,
        "message": f"Hello {name}!"
    }


@app.get("/add")
def add(a: int, b: int):
    return {
        "a": a,
        "b": b,
        "result": a + b
    }

# 3. डेटाबेस में डेटा सेव करने और देखने के नए रूट्स (ताकि चेक कर सकें)
@app.get("/get-db-data")
def get_db_data():
    try:
        items = list(collection.find({}, {"_id": 0}))
        return {"status": "success", "data": items}
    except Exception as e:
        return {"status": "error", "message": str(e)}
