from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
async def index() -> dict[str, str]:
    return {'hello' : 'world'}


@app.get('/about')
async def about() -> str:
    return 'An Exceptional company'



if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host='0.0.0.0', reload=True, log_level="info")
