from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from src.configs.database import get_session

DatabaseDependencys = Annotated[AsyncSession, Depends(get_session)]