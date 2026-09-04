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


# 3. 🌐 मुख्य रूट: यहाँ आपका पूरा फ्रंटएंड सीधे पाइथन के अंदर ही सुरक्षित रहेगा
@app.get("/", response_class=HTMLResponse)
def home():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>My Frontend App</title>
        <style>
            body { font-family: Arial, sans-serif; text-align: center; background-color: #f4f4f9; margin-top: 100px; }
            .card { background: white; padding: 30px; border-radius: 10px; display: inline-block; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
            h1 { color: #4a4a4a; }
            .btn { background-color: #4CAF50; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
            .btn:hover { background-color: #45a049; }
            #response { margin-top: 20px; font-weight: bold; color: #333; }
        </style>
    </head>
    <body>
    <div class="card">
        <h1>मेरा फ्रंटएंड ऐप 🌐</h1>
        <p>यह पेज रेलवे बैकएंड के अंदर से ही लाइव चल रहा है।</p>
        <button class="btn" onclick="checkBackend()">बैकएंड टेस्ट करें</button>
        <div id="response">बटन पर क्लिक करके रिस्पॉन्स देखें...</div>
    </div>
    <script>
        const BACKEND_URL = window.location.origin; // यह अपने आप रेलवे का लिंक पकड़ लेगा
        function checkBackend() {
            document.getElementById('response').innerText = "लोड हो रहा है...";
            fetch(`${BACKEND_URL}/hello`)
                .then(res => res.json())
                .then(data => {
                    document.getElementById('response').innerText = `सफलता! संदेश: ${data.message}`;
                    document.getElementById('response').style.color = "green";
                })
                .catch(err => {
                    document.getElementById('response').innerText = "कनेक्शन एरर!";
                    document.getElementById('response').style.color = "red";
                    console.error(err);
                });
        }
    </script>
    </body>
    </html>
    """
    return html_content


# 4. बाकी सारे वर्किंग रूट्स
@app.get("/hello")
def hello():
    return {"message": "Hello from Railway Backend! 🚀"}

@app.get("/user/{name}")
def user(name: str):
    return {"name": name, "message": f"Hello {name}!"}

@app.get("/add")
def add(a: int, b: int):
    return {"a": a, "b": b, "result": a + b}
