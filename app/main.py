from app.dependencies import get_db_gateway
from app.routers import activities


from fastapi import FastAPI, Depends

app = FastAPI(dependencies=[Depends(get_db_gateway)])


@app.on_event("startup")
def instantiate_db():
    # This will force the creation of a new MongoDBGateway object on startup
    get_db_gateway()


app.include_router(activities.router, prefix="/activities", tags=["Activities"])
