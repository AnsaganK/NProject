from pydantic import BaseModel, HttpUrl

class FieldSchema(BaseModel):
    name: str
    kadastrNumber: str
    coordinates: str
    urlShpFile: str
    shapeArea: str
    shapeLength: str
    districtId: str
