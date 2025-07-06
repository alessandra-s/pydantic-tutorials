from pydantic import BaseModel
from typing import Union, Optional

class MySecondModel(BaseModel): 
    first_name: str
    middle_name: Union [str, None] # Parameter doesn't haqve to be set