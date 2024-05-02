from typing import Annotated

from fastapi import Depends

from src.usecase.utils.unitofwork import IUnitOfWork, UnitOfWork

UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]
