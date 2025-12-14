from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class Product(Base):
    __tablename__ = 'vkusno_and_tochka_burgers'
    __table_args__ = {'schema':'public'}

    id: Mapped[int] = mapped_column(primary_key=True)
    image: Mapped[str]
    name: Mapped[str]
    weight_g: Mapped[int]
    calories_kkl: Mapped[int]
    nutritional_value_kj: Mapped[int]
    fats_g: Mapped[int]
    carbohydrates_g: Mapped[int]
    protein_g: Mapped[int]







