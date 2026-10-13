from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


# Define the structure of a note
class Notes(BaseModel):
    id: int
    title: str
    content: str


# Temporary in-memory storage
notes_storage = []


# POST: create a note
@app.post("/notes")
def create_note(note: Notes):
    notes_storage.append(note.model_dump())

    return {
        "message": "Note created successfully",
        "note": note
    }


# GET: get all notes
@app.get("/notes")
def get_all_notes():
    return notes_storage


# GET: get one note by id
@app.get("/notes/{note_id}")
def get_note(note_id: int):
    for note in notes_storage:
        if note["id"] == note_id:
            return note

    raise HTTPException(status_code=404, detail="Note not found")


# PUT: update a note by id
@app.put("/notes/{note_id}")
def update_note(note_id: int, updated_note: Notes):
    for index, note in enumerate(notes_storage):
        if note["id"] == note_id:
            notes_storage[index] = updated_note.model_dump()

            return {
                "message": "Note updated successfully",
                "note": updated_note
            }

    raise HTTPException(status_code=404, detail="Note not found")


# DELETE: delete a note by id
@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    for index, note in enumerate(notes_storage):
        if note["id"] == note_id:
            deleted_note = notes_storage.pop(index)

            return {
                "message": "Note deleted successfully",
                "note": deleted_note
            }

    raise HTTPException(status_code=404, detail="Note not found")