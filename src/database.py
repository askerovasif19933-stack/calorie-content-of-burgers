from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine
from src.config import DATABASE_URL


# движок для подключения
engine = create_engine(DATABASE_URL)


# базовый класс от которого наследуемся
class Base(DeclarativeBase):
    pass



# создаем фабрику сессий
get_session = sessionmaker(bind=engine, future=True)