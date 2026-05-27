from pydantic import BaseModel, ConfigDict, Field

class CategoryCreate(BaseModel):
    title: str = Field(..., examples=["Nome Categoria"])
    
class CategoryResponse(CategoryCreate):
    id: str  
    model_config = ConfigDict(from_attributes=True)