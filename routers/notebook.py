from fastapi import APIRouter
from pydantic import BaseModel

from engines.notebook import Notebook

router = APIRouter()


# / Models Dictionaries\

class AddEntryResponse (BaseModel):
    index: str
    id: str
    result: str


# / Requests and Response Models\

class EntryAddModel (BaseModel):
    status: str
    payload: AddEntryResponse

    class Config:
        schema_extra = {
            {
                "status": "success",
                "payload": {
                    "index": "notebook",
                    "id": "1607753673554",
                    "result": "created"
                }
            }
        }


class EntryModel(BaseModel):
    content: str

    class Config:
        schema_extra={
            "example": {
                "content": "Entry1"
            }
        }


@router.get("/api/notebook/entries", tags=["notebook"])
async def get_entries():
    return Notebook.get_entries()


@router.post("/api/notebook/entry", tags=["notebook"])
async def post_entry(entry: EntryModel):
    return Notebook.post_entry(entry)


@router.get("/api/notebook/{entry_id}", tags=["notebook"])
async def get_entry(entry_id: str):
    return Notebook.find_entry(entry_id)


@router.delete("/api/notebook/{entry_id}", tags=["notebook"])
async def delete_entry(entry_id: str):
    return Notebook.delete_entry(entry_id)

