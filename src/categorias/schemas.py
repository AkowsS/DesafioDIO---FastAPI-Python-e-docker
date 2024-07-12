from pydantic import Field, UUID4
from typing import Annotated
from src.contrib.schemas import BaseSchema

class CategoriaIn(BaseSchema):
  nome: Annotated[str, Field(description='Nome da categoria', example='Scale', max_length=10)]


class CategoriaOut(CategoriaIn):
  id: Annotated[UUID4, Field(description="Identificador da categoria")]