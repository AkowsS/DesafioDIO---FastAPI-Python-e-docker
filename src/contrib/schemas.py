from pydantic import BaseModel, Field, UUID4
from typing import Annotated
from datetime import datetime

class BaseSchema(BaseModel):
  class Config:
    extra = 'forbid'
    from_attributes = True

class OutMixin(BaseSchema):
  id: Annotated[UUID4, Field(description="Identificador")]
  created_at: Annotated[datetime, Field(description="Data de criação")]
