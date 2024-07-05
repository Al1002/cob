from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

import user_manager
import project_manager
import db_interface

# this file is only concerned with telling project manager to do things
# issue: project uses user to determine where to do its thing
# aka it needs to know what a project is AND what a user is
# dunno how to fix

#ENDPOINTS = {
#    'create_project': '/'
#}

PROJECT_TYPES = ("python", "java", "go")

class ProjectCreationRequest(BaseModel):
    name: str
    type: str | None

project_router = APIRouter()

#project creation request
@project_router.post("/user/{user}")
def create_project(user: str, project: ProjectCreationRequest):
    if not user_manager.user_exists(user):
        raise HTTPException(400, "User does not exist!")

#list of user projects
@project_router.get("/user/{user}")

#project upload
@project_router.post("/user/{user}/project/{project}")

#project state
@project_router.get("/user/{user}/project/{project}")

#start the project
@project_router.post("/user/{user}/project/{project}/run")
def run_project(user: str, project: str):
    id = project_manager.run_project_detached(user, project)
    return {"msg":"Project started", "uuid": id}

#runing state; result
@project_router.get("/user/{user}/project/{project}/run")
def get_result(user: str, project: str, uuid: str | None):
    result = db_interface.DBInterface.get_result(uuid)
    if result == None:
        return {"message": "Result not ready or does not exist"}
    return {"result": result}
