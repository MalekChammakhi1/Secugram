from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
 
 
 
class ImageOut(BaseModel):
    id:           str
    filename:     str
    content_type: str
    size_bytes:   int
    owner_id:     str
    uploaded_at:  datetime