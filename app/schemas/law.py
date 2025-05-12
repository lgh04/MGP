from pydantic import BaseModel

class LawResponse(BaseModel):
    title: str
    description: str
