from pydantic import BaseModel
from typing import Union

class Token(BaseModel):
    access_token: str
    token_type: str
    user: Union[dict, None] = None