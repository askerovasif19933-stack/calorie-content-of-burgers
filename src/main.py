
from sqlalchemy import select
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from database import get_session
from models import Product


app = FastAPI(title='информация о калорийности бургеров', description='API для получения информации о калорийности бургеров')


from fastapi.staticfiles import StaticFiles

from fastapi.staticfiles import StaticFiles

app.mount("/static", StaticFiles(directory="../static"), name="static")



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Pydantic — служит для валидации входных/выходных данных.
class Burger(BaseModel):
    image: Optional[str]
    name: str
    weight_g: int
    calories_kkl: int
    nutritional_value_kj: int
    fats_g: int
    carbohydrates_g: int
    protein_g: int
    
    class Config:
        orm_mode = True



# --- HTTP маршруты (эндпойнты) ---


@app.get("/")
def root():
    # Возвращаем HTML-файл как главную страницу
    return {"message": "Перейдите на /docs или /static/front.html"}


@app.get("/burgers/", response_model=List[Burger])
async def get_burgers():
    """Маршрут для получения списка всех бургеров с их калорийностью."""

    # Создаем сессию для взаимодействия с базой данных
    with get_session() as session:
        # Выполняем запрос для получения всех бургеров
        stmt = select(Product)
        burgers = session.execute(stmt).scalars().all()
        
        # Преобразуем результаты в список Pydantic моделей
        result = [
            Burger(
                image=burger.image,
                name=burger.name,
                weight_g=burger.weight_g,
                calories_kkl=burger.calories_kkl,
                nutritional_value_kj=burger.nutritional_value_kj,
                fats_g=burger.fats_g,
                carbohydrates_g=burger.carbohydrates_g,
                protein_g=burger.protein_g
            )
            for burger in burgers
        ]
        
        return result
    
@app.get("/burgers/search", response_model=Optional[Burger])
async def get_burger(name: str=''):
    """Маршрут для получения информации о конкретном бургере по его ID."""

    # Создаем сессию для взаимодействия с базой данных
    with get_session() as session:
        # Выполняем запрос для получения бургера по имени
        stmt = select(Product).where(Product.name.ilike(f"%{name}%"))
        burger = session.execute(stmt).scalars().first()

        if not burger:
            raise HTTPException(
            status_code=400,
            detail="Название бургера не может быть пустым"
        )

        # Преобразуем результат в Pydantic модель
        result = Burger(
            image=burger.image,
            name=burger.name,
            weight_g=burger.weight_g,
            calories_kkl=burger.calories_kkl,
            nutritional_value_kj=burger.nutritional_value_kj,
            fats_g=burger.fats_g,
            carbohydrates_g=burger.carbohydrates_g,
            protein_g=burger.protein_g
        ) 

        return result
    



