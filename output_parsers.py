
from langchain.output_parsers import PydanticOutputParser
from langchain_core.pydantic_v1 import BaseModel, Field

class Expertise(BaseModel):
    expertise: str = Field(description="The expertise of the person", example="Java")
    years_of_experience: int = Field(description="The years of experience of the person", example=5)

expertise_parser = PydanticOutputParser(pydantic_object=Expertise)