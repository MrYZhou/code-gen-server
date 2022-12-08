from typing import Optional

from sqlmodel import Field, Session, SQLModel

from db import engine


class Table(SQLModel, table=True):
    __tablename__: str = "food_menu"
    id: Optional[int] = Field(default=None, primary_key=True)
    menu_name: Optional[str] = Field(default=None)
    menu_img: Optional[str] = Field(default=None)
    menu_price: Optional[int] = Field(default=None)
    menu_status: str = Field(default=None)



def addFood():
    food = Table(menu_name="foods1", menu_status="1")
    with Session(engine) as session:
        session.add(food)
        session.commit()
