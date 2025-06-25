from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Patient Medical Record Management System"}
