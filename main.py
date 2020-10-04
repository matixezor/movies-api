from fastapi import FastAPI
import uvicorn

from routers import users, movies

app = FastAPI()

app.include_router(users.router, prefix='/users', tags=['users'])
# app.include_router(movies.router, prefix='/movies', tags=['movies'])

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
