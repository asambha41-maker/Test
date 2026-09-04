from fastapi import FastAPI

app = FastAPI(title="My Test Backend")


@app.get("/")
def home():
    return {
        "message": "Backend successfully deployed!",
        "status": "online"
    }


@app.get("/hello")
def hello():
    return {
        "message": "Hello from Render 🚀"
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