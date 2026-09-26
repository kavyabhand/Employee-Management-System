from pydantic import BaseModel, ConfigDict


class EmployeeCreate(BaseModel):
    name: str
    email: str
    department: str


class EmployeeUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    department: str | None = None


class EmployeeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    department: str
