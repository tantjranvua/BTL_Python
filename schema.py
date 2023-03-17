from pydantic import BaseModel

class Columns_Value (BaseModel):
	name: str
	value: str