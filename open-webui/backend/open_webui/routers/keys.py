
from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel
from typing import List, Optional
import uuid
import hashlib
import time
from litellm import Router as LiteLLMRouter
import logging

from open_webui.models.users import Users, UserModel
from open_webui.models.virtual_keys import VirtualKeys, VirtualKeyModel, CreateVirtualKeyForm
from open_webui.utils.auth import get_verified_user
from open_webui.internal.db import get_db

log = logging.getLogger(__name__)

router = APIRouter()

class KeyResponse(BaseModel):
    key: str
    key_hash: str
    user_id: str
    key_name: str
    budget_limit: float

@router.post("/generate", response_model=KeyResponse)
async def generate_key(form_data: CreateVirtualKeyForm, user=Depends(get_verified_user)):
    # Generate a new sk- key
    raw_key = f"sk-{uuid.uuid4().hex}"
    key_hash = hashlib.sha256(raw_key.encode()).hexdigest()
    
    # Ensure ID uniqueness
    key_id = uuid.uuid4().hex

    # Save to DB
    new_key = VirtualKeys.insert_new_key(
        id=key_id,
        user_id=user.id,
        key_hash=key_hash,
        key_name=form_data.key_name,
        budget_limit=form_data.budget_limit
    )

    if not new_key:
        raise HTTPException(status_code=500, detail="Failed to create virtual key")

    return KeyResponse(
        key=raw_key,
        key_hash=key_hash,
        user_id=new_key.user_id,
        key_name=new_key.key_name,
        budget_limit=new_key.budget_limit
    )

@router.get("/list", response_model=List[VirtualKeyModel])
async def list_keys(user=Depends(get_verified_user)):
    # Ideally we should filter by user_id in the DB query
    # For now, let's assume admin or implementation of get_keys_by_user_id
    # This is a placeholder implementation
    return [] 

