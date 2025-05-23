import uvicorn
from fastapi import FastAPI, HTTPException, Path, Query, Depends

from models import GenreURLChoices, Band, BandCreate, Album
from typing import Annotated
from db import init_db, get_session
from sqlmodel import Session, select



app = FastAPI()




BANDS = [
    {'id' : 1, 'name' : 'The Kinks', 'genre' : 'Rock'},
    {'id' : 2, 'name' : 'Aphex Twin', 'genre' : 'Electronic'},
    {'id' : 3, 'name' : 'Black Sabbath', 'genre' : 'Metal', 'albums':[{'title': 'Master of Reality', 'release_date': '1971-07-21'}]},
    {'id' : 4, 'name' : 'Wu-Tang Clan', 'genre' : 'Hip-Hop'},
]


@app.get("/bands")
async def bands(
    genre: GenreURLChoices | None = None,
    q: Annotated[str | None, Query(max_length=10)] = None,
    session: Session = Depends(get_session)
) -> list[Band]:
    
    band_list = session.exec(select(Band)).all()
    if genre:
        band_list = [
            b for b in band_list if b.genre.value.lower() == genre.value
        ]
    if q:
        band_list = [b for b in band_list if q.lower() in b.name.lower()]
    return band_list


@app.get('/bands/{band_id}')
async def band(
    band_id: Annotated[int, Path(title="The band ID")], 
    session: Session = Depends(get_session)
) -> Band:
    band = session.get(Band, band_id)
    if band is None:
        # status code 404
        raise HTTPException(status_code=404, detail='Band not found')
    return band


@app.post("/bands/")
async def create_band(
    band_data: BandCreate,
    session: Session = Depends(get_session)
    )-> Band:
    band = Band(name=band_data.name, genre=band_data.genre)
    session.add(band)

    if band_data.albums:
        for album in band_data.albums:
            album_obj = Album(
                title=album.title, release_date=album.release_date, band=band
                )
            session.add(album_obj)

    session.commit()
    session.refresh(band)
    return band



if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host='0.0.0.0', reload=True, log_level="info")
