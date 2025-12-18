
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from typing import List, Optional
from database import get_session
from models import Product
from fastapi.staticfiles import StaticFiles
from crud import main
from sevice import Burger, get_all_burgers, get_one_burger
main()


app = FastAPI(title='информация о калорийности бургеров', description='API для получения информации о калорийности бургеров')



# Подключение статических файлов

app.mount("/static", StaticFiles(directory="../static"), name="static")



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
async def index():
    """Возвращает главную страницу приложения."""
    with open("../static/front.html", "r", encoding="utf-8") as f:
        return f.read()


@app.get("/burgers/", response_model=List[Burger])
async def get_burgers():

        return await get_all_burgers()
    
@app.get("/burgers/search", response_model=Optional[Burger])
async def get_burger(name: str=''):

        return await get_one_burger(name=name)
    



