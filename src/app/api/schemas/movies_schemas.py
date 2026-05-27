from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional

class MovieCreate(BaseModel):
    title: str = Field(..., examples=["Batman: O Cavaleiro das Trevas"])
    description: str = Field(..., min_length=1)
    category_ids: List[str] = Field(..., examples=[["id_1", "id_2"]])
    price: float = Field(..., gt=0)
    year: str = Field(..., examples=["2012"])
    duration: str = Field(..., examples=["1h 30min"]) 
    image_url: Optional[str] = None
    url_movie: str = Field(..., examples=["https://www.youtube.com/watch?v=dQw4w9WgXcQ"])
    
class MovieUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category_ids: Optional[List[str]] = None
    price: Optional[float] = None
    year: Optional[str] = None
    duration: Optional[str] = None
    image_url: Optional[str] = None
    url_movie: Optional[str] = None

class MovieResponse(MovieCreate):
    id: str
    
    model_config = ConfigDict(
        from_attributes=True, 
        json_schema_extra={
            "example": {
                "id": "ID do filme",
                "title": "Titulo do filme",
                "description": "Sinopse do filme",
                "category_ids": ["id_1", "id_2"],
                "price": 29.90,
                "year": "2026",
                "duration": "1h 30min",
                "url_movie": "https://www.youtube.com/watch?v=ID_VIDEO",
                "image_url": "https://url_da_imagem.jpg"
            }
        }
    )
    
    