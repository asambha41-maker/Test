import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pymongo import MongoClient

app = FastAPI(title="Fresh Render Backend")

# 1. CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. MongoDB Connections
MONGO_URL = os.environ.get("MONGO_URL")
collection = None

try:
    if MONGO_URL:
        # एनवायरनमेंट वेरिएबल से कनेक्ट करें
        client = MongoClient(MONGO_URL)
        db = client["myDatabase"]
        collection = db["test_collection"]
        print("MongoDB Connected Successfully! 🎉")
    else:
        print("⚠️ MONGO_URL not configured yet.")
except Exception as e:
    print(f"Database connection error: {e}")


# 3. 🌐 LIVE FRONTEND PAGE (मुख्य रूट)
@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Render Fresh App</title>
        <style>
            body { font-family: 'Segoe UI', Arial, sans-serif; text-align: center; background: #eef2f3; margin-top: 100px; }
            .card { background: white; padding: 40px; border-radius: 12px; display: inline-block; box-shadow: 0 8px 16px rgba(0,0,0,0.1); max-width: 450px; }
            h1 { color: #333; margin-bottom: 10px; }
            p { color: #666; font-size: 15px; }
            .btn { background: #ff4757; color: white; padding: 12px 24px; border: none; border-radius: 25px; cursor: pointer; font-size: 16px; font-weight: bold; transition: 0.3s; }
            .btn:hover { background: #ff6b81; transform: scale(1.05); }
            #status-box { margin-top: 25px; padding: 12px; border-radius: 6px; font-weight: bold; background: #f1f2f6; }
        </style>
    </head>
    <body>
    <div class="card">
        <h1>Render Fresh Deploy! 🚀</h1>
        <p>यह आपका एकदम नया फ्रंटएंड और बैकएंड कॉम्बो है।</p>
        <button class="btn" onclick="testServer()">चेक करें</button>
        <div id="status-box">बटन दबाकर टेस्ट करें...</div>
    </div>

    <script>
        function testServer() {
            const box = document.getElementById('status-box');
            box.innerText = "लोड हो रहा है...";
            box.style.color = "#333";
            
            fetch(window.location.origin + '/hello')
                .then(res => res.json())
                .then(data => {
                    box.innerText = "✅ बैकएंड से रिस्पॉन्स: " + data.message;
                    box.style.color = "#2ed573";
                })
                .catch(err => {
                    box.innerText = "❌ कनेक्शन फेल!";
                    box.style.color = "#ff4757";
                    console.error(err);
                });
        }
    </script>
    </body>
    </html>
    """

# 4. टेस्ट एपीआई एंडपॉइंट
@app.get("/hello")
def hello():
    return {"message": "Hello World! आपका नया रेंडर सर्वर बिल्कुल सही चल रहा है।"}
