from pydantic import BaseModel, Field


class NoteInSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=64)
    description: str = Field(..., min_length=3, max_length=64)


class NoteSchema(NoteInSchema):
    id: int
