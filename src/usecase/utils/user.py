from dataclasses import dataclass
from enum import Enum
from fastapi import Depends, HTTPException, Request


class Roles(Enum):
    ADMIN = "ADMIN"
    MAIN_HR = "MAIN_HR"
    SUB_HR = "SUB_HR"
    STAFF = "STAFF"
    CHIEF = "CHIEF"
    DEPUTY_CHIEF = "DEPUTY_CHIEF"
    DEPARTMENT_HEAD = "DEPARTMENT_HEAD"
    COMMISSION_MEMBER = "COMMISSION_MEMBER"
    COMMISSION_HEAD = "COMMISSION_HEAD"
    EXECUTIVE_OFFICER = "EXECUTIVE_OFFICER"

@dataclass
class User:
    """
    User model is stored on external service, so we don't need to store it in our database.
    """

    id: int
    pinfl: str
    last_organization_id: int
    roles: list[Roles]
    organizations: list[int]

    def __post_init__(self):
        for role in self.roles:
            if role not in Roles._member_names_:
                raise ValueError(("Invalid role: %(role)s") % {"role": role})


async def get_current_user(request: Request) -> User:
    # Retrieve user object from request state
    user = request.state.user
    if user is None:
        # If user is not found, raise HTTPException with status code 401 (Unauthorized)
        raise HTTPException(status_code=401, detail="User not authenticated")
    return user