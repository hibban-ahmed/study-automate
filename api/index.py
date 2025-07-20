import os
from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from helper import call_ai_model
from dotenv import load_dotenv

load_dotenv()

# Current directory is where this file (e.g. api/index.py) is located
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Base project root (one level above 'api/')
BASE_DIR = os.path.dirname(CURRENT_DIR)

app = FastAPI()

# Static directory inside api folder
static_dir = os.path.join(CURRENT_DIR, "static")
if not os.path.isdir(static_dir):
    raise RuntimeError(f"Static directory not found: {static_dir}")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Templates directory at project root level
templates_dir = os.path.join(BASE_DIR, "templates")
if not os.path.isdir(templates_dir):
    raise RuntimeError(f"Templates directory not found: {templates_dir}")
templates = Jinja2Templates(directory=templates_dir)

API_KEYS = {
    "gemini": os.environ.get("GEMINI_API_KEY"),
    "llama": os.environ.get("LLAMA_API_KEY")
}
MAIN_API_KEY = os.environ.get("MAIN_API_KEY")

def verify_key(x_api_key: str = ""):
    if x_api_key != MAIN_API_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # Render your frontend.html template
    return templates.TemplateResponse("frontend.html", {"request": request})


@app.post("/ask")
async def ask_homework(
    prompt: str = Form(...),
    resources: str = Form(...),
    model: str = Form(...),
    x_api_key: str = Form(...)
):
    verify_key(x_api_key)
    api_key = API_KEYS.get(model)
    if not api_key:
        raise HTTPException(status_code=400, detail="Invalid model")

    result = await call_ai_model(prompt, resources, model=model, api_key=api_key)
    return {"result": result}
