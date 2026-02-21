from fastapi import FastAPI
from app.database import engine,Base
#important : on importe le modele pour que SQLALCHEMY le connaisse avant create_all
from app.models import user
from app.routers import auth

#on cree les tables 
Base.metadata.create_all(bind=engine)

app=FastAPI()

app.include_router(auth.router)

@app.get("/")
def read_root():
	return {"status":"API connected to PostgreSQL !"}
