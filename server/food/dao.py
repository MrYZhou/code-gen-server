from typing import Optional

from sqlmodel import Field, Session, SQLModel


class Table(SQLModel, table=True):
    __tablename__: str = "food_menu"
    id: Optional[int] = Field(default=None, primary_key=True)
    menu_name: Optional[str] = Field(default=None)
    menu_img: Optional[str] = Field(default=None)
    menu_price: Optional[int] = Field(default=None)
    menu_status: str = Field(default=None)


def addFood() -> None:
    food = Table(menu_name="foods1", menu_status="1")
    with Session(engine.get_db()) as session:
        session.add(food)
        session.commit()
