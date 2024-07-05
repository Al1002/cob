from fastapi import FastAPI, UploadFile, Body, HTTPException
#from pydantic import BaseModel
from typing_extensions import Annotated # For complex function signatures
from typing import List                 #

from project_package.projects_web_interface import project_router

app = FastAPI()
app.include_router(project_router)

@app.get("/")
async def root():
    return "<p>This is COB webserver. More info at [https://github.com/Al1002/cob]<\p>"


if __name__ == "__main__":
    pass

