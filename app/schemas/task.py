from pydantic import BaseModel
from typing import Optional

class TaskBase(BaseModel):
	title:str
	description:Optional[str]=None
	completed:bool=False

class TaskCreate(TaskBase):
	user_id:int


class TaskUpdate(BaseModel):
	title:Optional[str]=None
	description:Optional[str]=None
	completed:Optional[bool]=None
	user_id:Optional[int]=None

class Task(TaskBase):
	id:int
	user_id:int

	class config:
	    from_attribute=True
