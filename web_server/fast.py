from fastapi import FastAPI, UploadFile, Body, HTTPException
#from pydantic import BaseModel
from typing_extensions import Annotated # For complex function signatures
from typing import List                 #
import os # file operations
from pathlib import Path # path concatenation and code clarity
import uuid # for db/ticket system
from threading import Thread # independent runing of containers

from build_container import ContainerManager
from db_interface import DBInterface

USER_DIRECTORY = "/home/sasho_b/Coding/cob/users"

app = FastAPI()


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

@app.get("/")
async def root():
    return "<p>This is COB webserver<\p>"

@app.post("/{username}/code")
def upload_file(username: str, upload: UploadFile):
    error = validate_upload_file(upload)
    if error != None:
        raise HTTPException(
            status_code=400,
                detail=error,
            headers={"msg": "The file is invalid"}
        )
    
    error = save_upload_file(Path(USER_DIRECTORY, username), upload)
    if error != None:
        raise HTTPException(
            status_code=400,
            detail=error,
            headers={"msg": f"There was an error uploading '{upload.filename}' to user '{username}'"}
        )
    
    return {"message": f"Successfully uploaded '{upload.filename}' to user '{username}'"}


def post_files(username: str, uploads: List[UploadFile]):
    for upload in uploads:
        error = validate_upload_file(upload)
        if error != None:
            raise HTTPException(
                status_code=400,
                detail=error,
                headers={"msg": f"The file {upload.filename} is invalid. Dropping request."}
            )
    for upload in uploads:
        error = save_upload_file(Path(USER_DIRECTORY, username), upload)
        if error != None:
            raise HTTPException(
                status_code=400,
                detail=error,
                headers={"msg": f"There was an error uploading '{upload.filename}' to user '{username}'"}
            )
    
    return {"message": f"Successfully uploaded '{upload.filename}' to user '{username}'"}

@app.get("/{username}/code")
def get_code(username: str):
    return {
        "message": f"Files for user '{username}'",
        "files": os.listdir(Path(USER_DIRECTORY, username))
        }

@app.post("/{username}/run/{filename}")
def run_code(username: str, filename: str):
    if not os.path.isdir(Path(USER_DIRECTORY,username)):
        raise HTTPException(
            status_code=400,
            detail="User does not exist",
            headers={"msg": "Couldnt run code"}
            )
    if not os.path.exists(Path(USER_DIRECTORY,username,filename)):
        raise HTTPException(
            status_code=400,
            detail="File does not exist",
            headers={"msg": "Couldnt run code"}
            )
    id = ContainerManager.run_project(Path(USER_DIRECTORY,username,filename), source_dir=None, build_dir=Path(USER_DIRECTORY,username))
    return {"uuid":id}

@app.get("/{username}/result/{uuid}")
def get_result(username: str, uuid: str):
    result = DBInterface.get_result(uuid)
    if result == None:
        return {"message": "Result not ready or does not exist"}
    return {"result": result}

if __name__ == "__main__":
    id =run_code("john_doe", "hello.py")
    print(get_result("john_doe",id['uuid']))