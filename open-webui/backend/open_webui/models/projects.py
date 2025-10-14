import logging
import json
import time
import uuid
from typing import Optional, List
from enum import Enum

from open_webui.internal.db import Base, get_db, JSONField
from pydantic import BaseModel, ConfigDict
from sqlalchemy import BigInteger, Boolean, Column, String, Text
from sqlalchemy import or_, func, select, and_, text
from open_webui.models.chats import Chats, ChatModel

####################
# Project DB Schema
####################

class ProjectPermission(str, Enum):
    READ = "read"
    WRITE = "write"
    ADMIN = "admin"

class Project(Base):
    __tablename__ = "project"
    
    id = Column(String, primary_key=True)
    user_id = Column(String)  # Owner
    name = Column(String)
    description = Column(Text, nullable=True)
    color = Column(String, nullable=True)
    
    created_at = Column(BigInteger)
    updated_at = Column(BigInteger)
    
    # Sharing and permissions
    is_shared = Column(Boolean, default=False)
    share_permissions = Column(JSONField, server_default="{}")
    
    # Metadata and status
    meta = Column(JSONField, server_default="{}")
    archived = Column(Boolean, default=False)

class ProjectModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: str
    user_id: str
    name: str
    description: Optional[str] = None
    color: Optional[str] = None
    
    created_at: int
    updated_at: int
    
    is_shared: bool = False
    share_permissions: dict = {}
    meta: dict = {}
    archived: bool = False

####################
# Forms
####################

class ProjectForm(BaseModel):
    name: str
    description: Optional[str] = None
    color: Optional[str] = None

class ProjectUpdateForm(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None

class ProjectShareForm(BaseModel):
    user_ids: List[str]
    permission: ProjectPermission

####################
# Project Operations
####################

class ProjectTable:
    def insert_new_project(self, user_id: str, form_data: ProjectForm) -> Optional[ProjectModel]:
        with get_db() as db:
            id = str(uuid.uuid4())
            project = ProjectModel(
                id=id,
                user_id=user_id,
                name=form_data.name,
                description=form_data.description,
                color=form_data.color,
                created_at=int(time.time()),
                updated_at=int(time.time()),
            )
            
            result = Project(**project.model_dump())
            db.add(result)
            db.commit()
            db.refresh(result)
            return ProjectModel.model_validate(result) if result else None

    # Get chats by project_id already exists in chats.py

    def get_projects_by_user_id(self, user_id: str, include_shared: bool = True) -> List[ProjectModel]:
        with get_db() as db:
            query = db.query(Project)
            
            if include_shared:
                # Include projects owned by user OR shared with user
                query = query.filter(
                    or_(
                        Project.user_id == user_id,
                        text(f"JSON_EXTRACT(share_permissions, '$.{user_id}') IS NOT NULL")
                    )
                )
            else:
                query = query.filter_by(user_id=user_id)
            
            query = query.filter_by(archived=False).order_by(Project.updated_at.desc())
            projects = query.all()
            return [ProjectModel.model_validate(project) for project in projects]
    
    def get_project_by_id_and_user_id(self, id: str, user_id: str) -> Optional[ProjectModel]:
        with get_db() as db:
            project = db.query(Project).filter(
                Project.id == id,
                or_(
                    Project.user_id == user_id,
                    text(f"JSON_EXTRACT(share_permissions, '$.{user_id}') IS NOT NULL")
                )
            ).first()
            return ProjectModel.model_validate(project) if project else None
    
    def update_project_by_id(self, id: str, user_id: str, form_data: ProjectUpdateForm) -> Optional[ProjectModel]:
        with get_db() as db:
            project = db.query(Project).filter_by(id=id, user_id=user_id).first()
            if not project:
                return None
            
            if form_data.name is not None:
                project.name = form_data.name
            if form_data.description is not None:
                project.description = form_data.description
            if form_data.color is not None:
                project.color = form_data.color
            
            project.updated_at = int(time.time())
            db.commit()
            db.refresh(project)
            return ProjectModel.model_validate(project)
    
    def delete_project_by_id(self, id: str, user_id: str) -> bool:
        try:
            with get_db() as db:
                # Then delete the project
                db.query(Project).filter_by(id=id, user_id=user_id).delete()
                db.commit()
                print(f"Project deleted: {id}, {user_id}")
                return True
        except Exception as e:
            print(e)
            print(f"Error deleting project: {id}, {user_id}")
            return False

    def add_chat_to_project(self, project_id: str, chat_id: str, user_id: str) -> bool:
        try:
            with get_db() as db:
                result = Chats.update_chat_project_id_by_id_and_user_id(chat_id, user_id, project_id)
                print(f"add chat to project result: {result}")
                if result is None:
                    return False
                return True
        except Exception as e:
            print(e)
            print(f"Error adding chat to project: {project_id}, {chat_id}, {user_id}")
            return False
    
    def remove_chat_from_project(self, project_id: str, chat_id: str, user_id: str) -> bool:
        try:
            with get_db() as db:
                result = Chats.update_chat_project_id_by_id_and_user_id(chat_id, user_id, None)
                print(f"remove chat from project result: {result}")
                if result is None:
                    return False
                db.commit()
                return True
        except Exception as e:
            print(f"Error removing chat from project: {project_id}, {chat_id}, {user_id}")
            print(e)
            return False

    def update_chat_in_project(self, project_id: str, chat_id: str, user_id: str) -> Optional[ChatModel]:
        try:
            with get_db() as db:
                result = Chats.update_chat_folder_id_by_id_and_user_id(chat_id, user_id, project_id)
                print(f"update chat in project result: {result}")
                return result
        except Exception as e:
            print(f"Error updating chat in project: {project_id}, {chat_id}, {user_id}")
            print(e)
            return None

Projects = ProjectTable()