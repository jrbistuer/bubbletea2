from pydantic import BaseModel, ConfigDict, Field


class BubbleTeaBase(BaseModel):
    name: str = Field(..., max_length=100)
    temperature: str = Field(..., max_length=20)
    precio: float = Field(..., ge=0)
    active: bool = True


class BubbleTeaCreate(BubbleTeaBase):
    pass


class BubbleTeaUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=100)
    temperature: str | None = Field(default=None, max_length=20)
    precio: float | None = Field(default=None, ge=0)
    active: bool | None = None


class BubbleTeaRead(BubbleTeaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
