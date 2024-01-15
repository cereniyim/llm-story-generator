from app.routers import authentication, activities


from fastapi import FastAPI


app = FastAPI()

app.include_router(
    authentication.router, prefix="/authentication", tags=["Authentication"]
)
app.include_router(activities.router, prefix="/activities", tags=["Activities"])
