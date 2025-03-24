from fastapi import FastAPI, HTTPException
import uvicorn

app = FastAPI()

BANDS = [
    {'id' : 1, 'name' : 'The Kinks', 'genre' : 'Rock'},
    {'id' : 2, 'name' : 'Aphex Twin', 'genre' : 'Electronic'},
    {'id' : 3, 'name' : 'Slowdive', 'genre' : 'Shoegaze'},
    {'id' : 4, 'name' : 'Wu-Tang Clan', 'genre' : 'Hip-Hop'},
]


@app.get("/bands")
async def bands() -> list[dict]:
    return BANDS


@app.get('/bands/{band_id}')
async def band(band_id: int) -> dict:
    band = next((b for b in BANDS if b['id'] == band_id), None)
    if band is None:
        # status code 404
        raise HTTPException(status_code=404, detail='Band not found')
    return band




if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host='0.0.0.0', reload=True, log_level="info")
