import os # file operation
from pathlib import Path
import uuid
from threading import Thread

from containerizer import ContainerManager
from db_package import DBInterface
import user_package.user_manager as user_manager

def get_project_dir(user: str, project: str) -> Path:
    return Path(user_manager.get_user_dir(user), project)

def project_exists(user: str, project: str) -> bool:
    os.path.isdir(get_project_dir(user, project))

def create_project(user: str, project: str):
    os.mkdir(get_project_dir(user, project))

# TODO: CHANGE
def get_project_entry_file(user: str, project: str)->Path:
    return Path(get_project_dir(user, project), "main.py")

# TODO: FIX HACKJOB
# runs a project and saves its output to a database, along with an identifier for retrieval
def project_output_to_db(entry_file: Path, source_dir: Path, id: uuid.UUID) -> None:
    DBInterface.save_result({'uuid': str(id), "status": "running"})
    result = ContainerManager.run_project(entry_file, source_dir)
    DBInterface.results.update_one({'uuid': str(id)}, {"$set":{"status": "done", "result": result}})

# runs a project in a separate thread. returns an identifier for retrieval
def run_project_detached(user: str, project: str) -> uuid.UUID:
    id = uuid.uuid4()
    entry_file = get_project_entry_file(user, project)
    thread = Thread(target=project_output_to_db, args=[entry_file, user_manager.get_user_dir(user), id])
    thread.daemon = False
    thread.start()
    return id


