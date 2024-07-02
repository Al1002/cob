from fastapi import FastAPI, UploadFile, Body
from pydantic import BaseModel
from typing_extensions import Annotated
import os # file operations

save_directory = "/home/sasho_b/Coding/cob/web_server"

class Code(BaseModel):
    file_name: str

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/id/{id}")
async def id_method(id: int):
    return {"message": id}

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

@app.post("/upload_code/{username}")
def upload(username: str, upload: UploadFile):
    
    error = validate_upload_file(upload)
    if error:
        return {"message": f"The file is invalid", "details": error}
    
    error = save_upload_file(save_directory + "/" + username, upload)
    if error:
        return {"message": f"There was an error uploading '{upload.filename}' to user '{username}'", "details": error}
    
    return {"message": f"Successfully uploaded '{upload.filename}' to user '{username}'"}

if __name__ == "__main__":
    pass