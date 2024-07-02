from fastapi import FastAPI, UploadFile, Body, HTTPException
from pydantic import BaseModel
from typing_extensions import Annotated
import os # file operations
from pathlib import Path # path concatenation and code clarity

save_directory = "/home/sasho_b/Coding/cob/web_server"

class Code(BaseModel):
    file_name: str

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

def validate_upload_file(upload: UploadFile):
    if(upload.size > 1024*1024*5):
        return "Filesize exceeds 5MB"
    if(upload.filename == None):
        return "File doesnt have a name"
    return None

def save_upload_file(dir: str, upload: UploadFile):
    contents = upload.file.read() # read() does all the memory mumbo-jumbo
    if not os.path.exists(dir):
        os.makedirs(dir)
    try:
        f = open(dir + "/" + upload.filename, 'w+b')
        f.write(contents)
    except Exception:
        return "Couldnt write to file"
    finally:
        upload.file.close()    
    return None

@app.post("/{username}/code")
def post_code(username: str, upload: UploadFile):
    
    error = validate_upload_file(upload)
    if error:
        raise HTTPException(
            status_code=400,
            detail=error,
            headers={"msg": "The file is invalid"}
            )    
    
    error = save_upload_file(save_directory + "/" + username, upload)
    if error:
        raise HTTPException(
            status_code=400,
            detail=error,
            headers={"msg": f"There was an error uploading '{upload.filename}' to user '{username}'"}
            )
    
    return {"message": f"Successfully uploaded '{upload.filename}' to user '{username}'"}

@app.get("/{username}/code")
def get_code(username: str):
    return os.listdir(Path(save_directory, username))

@app.post("/{username}/run/{filename}")
def run_code(username: str, filename: str):
    if not os.path.isdir(Path(save_directory,username)):
        raise HTTPException(
            status_code=400,
            detail="User does not exist",
            headers={"msg": "Couldnt run code"}
            )
    if not os.path.exists(Path(save_directory,username,filename)):
        raise HTTPException(
            status_code=400,
            detail="File does not exist",
            headers={"msg": "Couldnt run code"}
            )


if __name__ == "__main__":
    pass