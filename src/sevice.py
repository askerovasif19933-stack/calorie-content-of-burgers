from typing import Optional
from pydantic import BaseModel  
from sqlalchemy import select
from database import get_session    
from models import Product




#Pydantic — служит для валидации входных/выходных данных.
class Burger(BaseModel):
    """Модель данных для бургера."""
    image: Optional[str]
    name: str
    weight_g: int
    calories_kkl: int
    nutritional_value_kj: int
    fats_g: int
    carbohydrates_g: int
    protein_g: int
    


async def get_all_burgers():    
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
    

async def get_one_burger(name: str=''):
    """Маршрут для получения информации о конкретном бургере по его ID."""

    # Создаем сессию для взаимодействия с базой данных
    with get_session() as session:
        # Выполняем запрос для получения бургера по имени
        stmt = select(Product).where(Product.name.ilike(f"%{name}%"))
        burger = session.execute(stmt).scalars().first()

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