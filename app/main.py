from fastapi import FastAPI
from app.database import engine,Base
#important : on importe le modele pour que SQLALCHEMY le connaisse avant create_all
from app.models import user
from app.routers import auth,users,tasks

#on cree les tables 
Base.metadata.create_all(bind=engine)

app=FastAPI()

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tasks.router)

@app.get("/")
def read_root():
	return {"status":"API connected to PostgreSQL !"}
