from enum import Enum
from pydantic import BaseModel, field_validator
from datetime import date

class GenreURLChoices(Enum):
    ROCK = 'rock'
    ELECTRONIC = 'electronic'
    METAL = 'metal'
    HIP_HOP = 'hip-hop'


class GenreChoices(Enum):
    ROCK = 'Rock'
    ELECTRONIC = 'Electronic'
    METAL = 'Metal'
    HIP_HOP = 'Hip-Hop'


class Album(BaseModel):
    title: str
    release_date: date


class BandBase(BaseModel):
    name: str
    genre: GenreChoices
    albums: list[Album] = []


class BandCreate(BandBase):
    @field_validator('genre', mode='before')
    def title_case_genre(cls, value):
        return value.title()


class BandWithID(BandBase):
    id: int


    