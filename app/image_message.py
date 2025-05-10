from pydantic import BaseModel, validator
from typing import Dict, Any
import base64


class ImageMessage(BaseModel):
    image_base64: str
    metadata: Dict[str, Any]

    @validator('image_base64')
    def validate_base64(cls, v):
        try:
            base64.b64decode(v, validate=True)
            return v
        except Exception:
            raise ValueError("image_base64 is not a valid base64 string")
