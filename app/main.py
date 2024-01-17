from app.routers import activities


from fastapi import FastAPI


app = FastAPI()

app.include_router(activities.router, prefix="/activities", tags=["Activities"])
