from pydantic import BaseModel,Field
from app.main import ExtractRequest, LeadFields

class FieldTypeKeys(BaseModel):
    explicit: list[str]
    derived: list[str]

class FixtureCase(BaseModel):
    id:str
    category:str
    input:ExtractRequest
    expected:LeadFields
    field_types:FieldTypeKeys
