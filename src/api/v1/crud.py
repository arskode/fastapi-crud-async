from src.api.v1.schema import NoteInSchema, NoteSchema
from src.api.v1.tables import notes
from src.extensions import database


async def post(payload: NoteInSchema):
    query = notes.insert().values(
        title=payload.title, description=payload.description
    )
    return await database.execute(query=query)


async def get(note_id: int):
    query = notes.select().where(notes.c.id == note_id)
    return await database.fetch_one(query=query)


async def get_all():
    query = notes.select()
    return await database.fetch_all(query=query)


async def put(note_id: int, payload: NoteSchema):
    query = (
        notes.update()
        .where(notes.c.id == note_id)
        .values(title=payload.title, description=payload.description)
        .returning(notes.c.id)
    )
    return await database.execute(query=query)


async def delete(note_id: int):
    query = notes.delete().where(notes.c.id == note_id).returning(notes.c.id)
    return await database.execute(query=query)
