from app.routers import auth
from app.routers import tasks
from fastapi import FastAPI
from app.database import engine,Base
#important : on importe le modele pour que SQLALCHEMY le connaisse avant create_all
from app.models import user
from app.routers import users
from app.core.logging import logger
import time

#on cree les tables 
Base.metadata.create_all(bind=engine)

app=FastAPI()

#middleware pour logger tous les requettes
@app.middleware("http")
async def log_requests(request,call_next):
	start_time=time.time()

	#Log la requette entrante
	logger.info(f"Requette:{request.method} {request.url.path}")

	response=await call_next(request)

	#Log la reponse
	process_time=time.time()-start_time
	logger.info(f"Reponse : {response.status_code}-{process_time:.3f}s")

	return response


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tasks.router)

@app.get("/")
def read_root():
	return {"status":"API connected to PostgreSQL !"}