from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from open_webui.models.projects import (
    Projects,
    ProjectModel,
    ProjectForm,
    ProjectUpdateForm,
    ProjectShareForm,
)
from open_webui.models.chats import Chats
from open_webui.utils.auth import get_verified_user
from open_webui.models.users import UserModel

router = APIRouter()

############################
# Project Management
############################

@router.get("/", response_model=List[ProjectModel])
async def get_projects(user=Depends(get_verified_user)):
    """Get all projects for the current user"""
    return Projects.get_projects_by_user_id(user.id)

@router.post("/", response_model=ProjectModel)
async def create_project(
    form_data: ProjectForm, user=Depends(get_verified_user)
):
    """Create a new project"""
    project = Projects.insert_new_project(user.id, form_data)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create project"
        )
    return project

@router.get("/{project_id}", response_model=ProjectModel)
async def get_project_by_id(
    project_id: str, user=Depends(get_verified_user)
):
    """Get a specific project by ID"""
    project = Projects.get_project_by_id_and_user_id(project_id, user.id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return project

@router.patch("/{project_id}", response_model=ProjectModel)
async def update_project_by_id(
    project_id: str,
    form_data: ProjectUpdateForm,
    user=Depends(get_verified_user)
):
    """Update a project"""
    project = Projects.update_project_by_id(project_id, user.id, form_data)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found or access denied"
        )
    return project

@router.delete("/{project_id}")
async def delete_project_by_id(
    project_id: str, user=Depends(get_verified_user)
):
    """Delete a project"""
    success = Projects.delete_project_by_id(project_id, user.id) and Chats.delete_chats_by_user_id_and_folder_id(user.id, project_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found or access denied"
        )
    return {"message": "Project deleted successfully"}

@router.get("/{project_id}/chats")
async def get_project_chats(
    project_id: str, user=Depends(get_verified_user)
):
    """Get all chats in a project"""
    # Verify user has access to project
    chats = Chats.get_chats_by_folder_id_and_user_id(project_id, user.id)
    if not chats:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found or access denied"
        )
    return chats


@router.post("/{project_id}/chats/{chat_id}")
async def add_chat_to_project(
    project_id: str,
    chat_id: str,
    user=Depends(get_verified_user)
):
    """Add a chat to a project"""
    chat = Projects.add_chat_to_project(project_id, chat_id, user.id)
    print(f"Chat added to project: {chat_id}, {project_id}, {user.id}")
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found or access denied"
        )
    return chat

@router.patch("/{project_id}/chats/{chat_id}")
async def remove_chat_from_project(
    project_id: str,
    chat_id: str,
    user=Depends(get_verified_user)
):
    """Remove a chat in a project"""
    chat = Projects.remove_chat_from_project(project_id, chat_id, user.id)
    print(f"Chat updated in project: {chat_id}, {project_id}, {user.id}")
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found or access denied"
        )
    return chat


@router.delete("/{project_id}/chats/{chat_id}")
async def remove_chat_from_project(
    project_id: str,
    chat_id: str,
    user=Depends(get_verified_user)
):
    """Remove a chat from a project"""
    chat = Projects.remove_chat_from_project(project_id, chat_id, user.id)
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found or access denied"
        )
    return chat