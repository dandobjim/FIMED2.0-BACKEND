from pydantic import BaseModel


class Form(BaseModel):
    id: str
    data_structure: dict

