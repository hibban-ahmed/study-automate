import os
from fastapi import FastAPI, Form, Request, Depends, HTTPException ## fastapi, data parameters in post requests, represents incoming http request, dependency injection
from fastapi.responses import HTMLResponse ## html content lata he
from fastapi.staticfiles import StaticFiles ## serves static files
from fastapi.templating import Jinja2Templates ##helps in rendering html templates
from AI_app.Ai_stuff import call_ai_model ## AI wala stuff isme he
from dotenv import load_dotenv
load_dotenv()



app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static") ##serves for static files
templates = Jinja2Templates(directory="templates") ##get html templates from template directory

API_KEYS = {
    "gemini": os.environ.get("GEMINI_API_KEY"),
    "llama": os.environ.get("LLAMA_API_KEY")
}
MAIN_API_KEY = os.environ.get("MAIN_API_KEY")


def verify_key(x_api_key: str = ""): ## a function taking only one string input 
    if x_api_key != MAIN_API_KEY: ## check karta he if they both match
        raise HTTPException(status_code=403, detail="Unauthorized") ## if conditions match than show error

@app.get("/", response_class=HTMLResponse)## root handles the html responses after fetrequests
async def home(request: Request):
    return templates.TemplateResponse("frontend.html", {"request": request}) ##frontend html file process and return karta he

@app.post("/ask") ##information lega user se
async def ask_homework(
    prompt: str = Form(...),
    resources: str = Form(...),
    model: str = Form(...),
    x_api_key: str = Form(...)
):
    verify_key(x_api_key)
    api_key = API_KEYS.get(model) ##jo model select hua he us se request karega ab
    if not api_key:
        raise HTTPException(status_code=400, detail="Invalid model") ##model agar galat ya nahi select hua

    result = await call_ai_model(prompt, resources, model=model, api_key=api_key)
    return {"result": result} ##upar wale variable wala result isme daal kar pass kardega