import json

from database import get_session, engine, Base
from models import Product
from logger import get_logger

logger = get_logger(__name__)

def json_pars():
    with open('../pars/vkusno_tochka_burger.json', 'r', encoding='utf-8') as f:
        src = json.load(f)
        return src

def crate_table():
    """Создание таблицы Product"""
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)



def insert(src):
    """Вставка данных в таблицу Product"""
    with get_session() as session:

        for k,v in src.items():

            insert_value = Product(
            image = v['image'],
            name = k,
            weight_g = float(v['масса']),
            calories_kkl =  float(v['Калории']),
            nutritional_value_kj = float(v['Пищевая ценность']),
            fats_g = float(v['Жиры'].split('_')[0]),
            carbohydrates_g = float(v['Углеводы']),
            protein_g = float(v['Белки'])
            )
            session.add(insert_value)
        session.commit()
    logger.info(f'{len(src)} данных вставлено')

def main():
    try:
        crate_table()

        src=json_pars()

        insert(src)

    except Exception as e:
        logger.error(e)