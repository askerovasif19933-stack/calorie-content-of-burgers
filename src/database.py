from  sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine
from config import host, password, port, user, db_name, url_ini


# движок для подключения
engine = create_engine(f"postgresql+psycopg2://{user}:{password}@{host}/{db_name}")



# базовый класс от которого наследуемся
class Base(DeclarativeBase):
    pass



# создаем фабрику сессий
get_session = sessionmaker(bind=engine, future=True)