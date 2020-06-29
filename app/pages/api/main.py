import scripts.bd_connection as mongoDB
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from scripts.bd_connection import MongoConecction
from starlette.responses import RedirectResponse


app = FastAPI()
templates = Jinja2Templates(directory="pages/public")

mongoDB = MongoConecction()
tempdir = "Data"


@app.get("/")
async def root(request:Request):
    return templates.TemplateResponse("index.html",{"request":request})


@app.post("/register")
async def register(usuario:str, password:str):
    mongoDB.crearClinico(usuario, password)
    return "ok"


@app.get("/sesion")
async def validate(request:Request):
    return templates.TemplateResponse("validate.html",{"request":request})


@app.post("/sesion")
async def envio_sesion(usuario:str, password:str):
    validado = mongoDB.validarClinico(usuario, password)
    if validado['correcto']:
        id = validado["id"]
        response = RedirectResponse(url='/home/{id}')
        return response
    else:
        response = RedirectResponse(url='/sesion')
        return response

