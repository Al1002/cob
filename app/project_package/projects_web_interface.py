from fastapi import APIRouter, HTTPException, UploadFile
from pydantic import BaseModel
from typing_extensions import Annotated, Union
import os
from pathlib import Path

import user_package.user_manager as user_manager
import project_package.project_manager as project_manager
from db_package import DBInterface

# this file is only concerned with telling project manager to do things
# issue: project uses user to determine where to do its thing
# aka it needs to know what a project is AND what a user is
# dunno how to fix

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
    project_manager.create_project(user, project.name)
    return {"msg": f"Project '{project.name}' created"}

#list of user projects
#@project_router.get("/user/{user}")

def validate_upload_file(upload: UploadFile):
    valid_upload_suffix = (".py")
    if upload.size > 1024*1024*5:
        return "Filesize exceeds 5MB"
    if upload.filename == None:
        return "File doesnt have a name"
    if not upload.filename.endswith(valid_upload_suffix):
        return "File type not allowed"
    return None

def save_upload_file(upload_dir: Path, upload: UploadFile):
    contents = upload.file.read() # read() does all the memory mumbo-jumbo
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    try:
        f = open(Path(upload_dir, upload.filename), 'w+b')
        f.write(contents)
    except Exception:
        return "Couldnt write to file"
    finally:
        upload.file.close()    
    return None

#project upload
@project_router.post("/user/{user}/project/{project}")
def upload_file(user: str, project: str, upload: UploadFile):
    error = validate_upload_file(upload)
    if error != None:
        raise HTTPException(400, detail=error, headers={"msg": "The file is invalid"})
    
    error = save_upload_file(Path(user_manager.get_user_dir(user), project), upload)
    if error != None:
        raise HTTPException(500,detail=error,headers={"msg": f"There was an error uploading '{upload.filename}' to user '{user}'"})
    
    return {"message": f"Successfully uploaded '{upload.filename}' to user '{user}'"}

#project state
#@project_router.get("/user/{user}/project/{project}")

#start the project
@project_router.post("/user/{user}/project/{project}/run")
def run_project(user: str, project: str):
    id = project_manager.run_project_detached(user, project)
    return {"msg":"Project started", "uuid": str(id)}

#runing state; result
@project_router.get("/user/{user}/project/{project}/run")
def get_result(user: str, project: str, uuid: Union[str | None] = None):
    result = DBInterface.get_result(uuid)
    if result == None:
        raise HTTPException(400, "Result not does not exist")
    if result['status'] == 'running':
        return {"msg": "Waiting for result"}
    if result['status'] == 'done':
        return {"result": result['result']}

if __name__ == '__main__':
    run_project("john_doe", "myproject")