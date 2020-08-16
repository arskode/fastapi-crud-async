from typing import List

from fastapi import APIRouter, HTTPException, Path, Response

from src.api.v1 import crud
from src.api.v1.schema import NoteInSchema, NoteSchema

router = APIRouter()


@router.post("/notes", response_model=NoteSchema, status_code=201)
async def create_note(payload: NoteInSchema):
    note_id = await crud.post(payload)
    return {
        "id": note_id,
        "title": payload.title,
        "description": payload.description,
    }


@router.get("/notes/{note_id}", response_model=NoteSchema)
async def read_note(note_id: int = Path(..., gt=0)):
    note = await crud.get(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.get("/notes", response_model=List[NoteSchema])
async def read_all_notes():
    return await crud.get_all()


@router.put("/notes/{note_id}", response_model=NoteSchema)
async def update_note(
    payload: NoteInSchema, note_id: int = Path(..., gt=0),
):
    note_id = await crud.put(note_id, payload)
    if not note_id:
        raise HTTPException(status_code=404, detail="Note not found")

    return {
        "id": note_id,
        "title": payload.title,
        "description": payload.description,
    }


@router.delete("/notes/{note_id}", status_code=204, response_class=Response)
async def delete_note(note_id: int = Path(..., gt=0)):
    note_id = await crud.delete(note_id)
    if not note_id:
        raise HTTPException(status_code=404, detail="Note not found")
    return
