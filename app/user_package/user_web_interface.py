from fastapi import APIRouter, HTTPException, UploadFile
from pydantic import BaseModel
from typing_extensions import Annotated, Union
import os
from pathlib import Path

import app.user_package.user_manager as user_manager
import project_package.project_manager as project_manager
from db_package import DBInterface

user_router = APIRouter()
