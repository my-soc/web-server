from fastapi import APIRouter
from pydantic import BaseModel
from engines.wave import Wave

router = APIRouter()


# Models

class VersionResponse(BaseModel):
    version: str


class VersionResponseModel(BaseModel):
    status: str
    payload: VersionResponse

    class Config:
        schema_extra = {
            "example": {
                "status": "success",
                "payload": {
                    "Version": "1.0"
                }
            }
        }


# Endpoints


@router.get("/", response_model=VersionResponseModel, tags=["root"])
def return_version():
    return Wave.get_version()
