from fastapi import FastAPI, UploadFile, Body, HTTPException
from pydantic import BaseModel
from typing_extensions import Annotated
import os # file operations
from pathlib import Path # path concatenation and code clarity
import build_container

user_directory = "/home/sasho_b/Coding/cob/web_server/users"

app = FastAPI()

@app.get("/")
async def root():
    return "<p>This is COB webserver<\p>"


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

@app.post("/{username}/code")
def post_code(username: str, upload: UploadFile):
    
    error = validate_upload_file(upload)
    if error != None:
        raise HTTPException(
            status_code=400,
            detail=error,
            headers={"msg": "The file is invalid"}
            )    
    
    error = save_upload_file(Path(user_directory, username), upload)
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
        "files": os.listdir(Path(user_directory, username))
        }

@app.post("/{username}/run/{filename}")
def run_code(username: str, filename: str):
    if not os.path.isdir(Path(user_directory,username)):
        raise HTTPException(
            status_code=400,
            detail="User does not exist",
            headers={"msg": "Couldnt run code"}
            )
    if not os.path.exists(Path(user_directory,username,filename)):
        raise HTTPException(
            status_code=400,
            detail="File does not exist",
            headers={"msg": "Couldnt run code"}
            )
    result = build_container.run_code(Path(user_directory,username,filename))
    return {"result": result}

if __name__ == "__main__":
    run_code("john_doe", "hello.py")