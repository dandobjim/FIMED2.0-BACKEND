from pydantic import BaseModel
from typing import List


class Row(BaseModel):
    name: str
    rtype: str


class Form(BaseModel):
    rows: List[Row]

