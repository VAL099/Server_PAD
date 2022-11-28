from pydantic import BaseModel

class Advert(BaseModel):
    category:str | None = None
    title:str | None = None
    description:str | None = None
    price:int | None = None