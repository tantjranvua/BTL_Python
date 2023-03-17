from pydantic import BaseModel

class Columns_Value (BaseModel):
	name: str
	value: str
class Number_Smoking (BaseModel):
	people: int
	age: int
class Smoking_Dead (BaseModel):
	people: int