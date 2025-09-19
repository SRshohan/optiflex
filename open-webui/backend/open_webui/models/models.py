import logging
import time
from typing import Optional
import os
from open_webui.internal.db import Base, JSONField, get_db
from open_webui.env import SRC_LOG_LEVELS

from open_webui.models.users import Users, UserResponse


from pydantic import BaseModel, ConfigDict

from sqlalchemy import or_, and_, func
from sqlalchemy.dialects import postgresql, sqlite
from sqlalchemy import BigInteger, Column, Text, JSON, Boolean


from open_webui.utils.access_control import has_access


log = logging.getLogger(__name__)
log.setLevel(SRC_LOG_LEVELS["MODELS"])

MODEL_ICON_PATTERNS = {
    'gpt-': '/static/icons/openai.png',
    'claude-': '/static/icons/anthropic.png',
    'gemini-': '/static/icons/gemini.png',
    'llama': '/static/icons/llama.png',
    'mistral-': '/static/icons/mistral.png',
    'cohere-': '/static/icons/cohere.png',
    'qwen-': '/static/icons/alibaba.png',
    'yi-': '/static/icons/01ai.png',
    'deepseek-': '/static/icons/deepseek.png'
    }
def check_icon_exists(icon_url: str) -> bool:
    for pattern, icon_url in MODEL_ICON_PATTERNS.items():
        if pattern in icon_url:
            return os.path.exists(icon_url)
    return False    



def get_model_icon_by_pattern(model_name: str, existing_icon: str = None) -> str:
    """Get model icon based on name pattern matching"""
    # If model already has a custom icon, use it
    # if existing_icon and existing_icon != '/static/favicon.png':
    #     return existing_icon
    
    # Pattern matching
    model_name_lower = model_name.lower()
    for pattern, icon_url in MODEL_ICON_PATTERNS.items():
        if pattern in model_name_lower:
            print(check_icon_exists(icon_url))
            return icon_url
    
    return '/static/favicon.png'  # fallback

####################
# Models DB Schema
####################


# ModelParams is a model for the data stored in the params field of the Model table
class ModelParams(BaseModel):
    model_config = ConfigDict(extra="allow")
    pass


# ModelMeta is a model for the data stored in the meta field of the Model table
class ModelMeta(BaseModel):
    profile_image_url: Optional[str] = "/static/favicon.png"

    description: Optional[str] = None
    """
        User-facing description of the model.
    """

    capabilities: Optional[dict] = None

    model_config = ConfigDict(extra="allow")

    pass


class Model(Base):
    __tablename__ = "model"

    id = Column(Text, primary_key=True)
    """
        The model's id as used in the API. If set to an existing model, it will override the model.
    """
    user_id = Column(Text)

    base_model_id = Column(Text, nullable=True)
    """
        An optional pointer to the actual model that should be used when proxying requests.
    """

    name = Column(Text)
    """
        The human-readable display name of the model.
    """

    params = Column(JSONField)
    """
        Holds a JSON encoded blob of parameters, see `ModelParams`.
    """

    meta = Column(JSONField)
    """
        Holds a JSON encoded blob of metadata, see `ModelMeta`.
    """

    access_control = Column(JSON, nullable=True)  # Controls data access levels.
    # Defines access control rules for this entry.
    # - `None`: Public access, available to all users with the "user" role.
    # - `{}`: Private access, restricted exclusively to the owner.
    # - Custom permissions: Specific access control for reading and writing;
    #   Can specify group or user-level restrictions:
    #   {
    #      "read": {
    #          "group_ids": ["group_id1", "group_id2"],
    #          "user_ids":  ["user_id1", "user_id2"]
    #      },
    #      "write": {
    #          "group_ids": ["group_id1", "group_id2"],
    #          "user_ids":  ["user_id1", "user_id2"]
    #      }
    #   }

    is_active = Column(Boolean, default=True)

    updated_at = Column(BigInteger)
    created_at = Column(BigInteger)


class ModelModel(BaseModel):
    id: str
    user_id: str
    base_model_id: Optional[str] = None

    name: str
    params: ModelParams
    meta: ModelMeta

    access_control: Optional[dict] = None

    is_active: bool
    updated_at: int  # timestamp in epoch
    created_at: int  # timestamp in epoch

    model_config = ConfigDict(from_attributes=True)


####################
# Forms
####################


class ModelUserResponse(ModelModel):
    user: Optional[UserResponse] = None


class ModelResponse(ModelModel):
    pass


class ModelForm(BaseModel):
    id: str
    base_model_id: Optional[str] = None
    name: str
    meta: ModelMeta
    params: ModelParams
    access_control: Optional[dict] = None
    is_active: bool = True


class ModelsTable:
    def insert_new_model(
        self, form_data: ModelForm, user_id: str
    ) -> Optional[ModelModel]:
        model = ModelModel(
            **{
                **form_data.model_dump(),
                "user_id": user_id,
                "created_at": int(time.time()),
                "updated_at": int(time.time()),
            }
        )
        try:
            with get_db() as db:
                result = Model(**model.model_dump())
                db.add(result)
                db.commit()
                db.refresh(result)

                if result:
                    return ModelModel.model_validate(result)
                else:
                    return None
        except Exception as e:
            log.exception(f"Failed to insert a new model: {e}")
            return None

    def get_all_models(self) -> list[ModelModel]:
        with get_db() as db:
            models = []
            updated_count = 0
            
            for model in db.query(Model).all():
                # Apply pattern matching and update database if needed
                current_meta = model.meta or {}
                current_icon = current_meta.get('profile_image_url', '/static/favicon.png')
                new_icon = get_model_icon_by_pattern(model.name, current_icon)

                print(f"Model: {model.name}")
                print(f"current_icon: {current_icon}")
                print(f"new_icon: {new_icon}")
                
                # Update database if icon changed
                if new_icon != current_icon:
                    # Use explicit SQL update instead of object modification
                    current_meta['profile_image_url'] = new_icon
                    db.query(Model).filter(Model.id == model.id).update({
                        'meta': current_meta,
                        'updated_at': int(time.time())
                    })
                    updated_count += 1
                    print(f"Updated model {model.name} with icon {new_icon}")
                
                models.append(ModelModel.model_validate(model))
            
            if updated_count > 0:
                db.commit()  # Commit all changes at once
                print(f"Committed {updated_count} model updates to database")
            else:
                print("No models needed updating")
            
            return models
            # return [ModelModel.model_validate(model) for model in db.query(Model).all()]

    def get_models(self) -> list[ModelUserResponse]:
        with get_db() as db:
            models = []
            updated_count = 0
            
            for model in db.query(Model).filter(Model.base_model_id != None).all():
                # Apply pattern matching and update database if needed
                current_meta = model.meta or {}
                current_icon = current_meta.get('profile_image_url', '/static/favicon.png')
                new_icon = get_model_icon_by_pattern(model.name, current_icon)
                
                # Update database if icon changed
                if new_icon != current_icon:
                    # Use explicit SQL update instead of object modification
                    current_meta['profile_image_url'] = new_icon
                    db.query(Model).filter(Model.id == model.id).update({
                        'meta': current_meta,
                        'updated_at': int(time.time())
                    })
                    updated_count += 1
                    print(f"Updated model {model.name} with icon {new_icon}")
                
                user = Users.get_user_by_id(model.user_id)
                models.append(
                    ModelUserResponse.model_validate(
                        {
                            **ModelModel.model_validate(model).model_dump(),
                            "user": user.model_dump() if user else None,
                        }
                    )
                )
            
            if updated_count > 0:
                db.commit()  # Commit all changes at once
                print(f"Committed {updated_count} model updates to database")
            
            return models
            

    def get_base_models(self) -> list[ModelModel]:
        with get_db() as db:
            return [
                ModelModel.model_validate(model)
                for model in db.query(Model).filter(Model.base_model_id == None).all()
            ]

    def get_models_by_user_id(
        self, user_id: str, permission: str = "write"
    ) -> list[ModelUserResponse]:
        models = self.get_models()
        return [
            model
            for model in models
            if model.user_id == user_id
            or has_access(user_id, permission, model.access_control)
        ]

    def get_model_by_id(self, id: str) -> Optional[ModelModel]:
        try:
            with get_db() as db:
                model = db.get(Model, id)
                if model:
                    # Apply pattern matching and update database if needed
                    current_meta = model.meta or {}
                    current_icon = current_meta.get('profile_image_url', '/static/favicon.png')
                    new_icon = get_model_icon_by_pattern(model.name, current_icon)
                    
                    # Update database if icon changed
                    if new_icon != current_icon:
                        # Use explicit SQL update instead of object modification
                        current_meta['profile_image_url'] = new_icon
                        db.query(Model).filter(Model.id == id).update({
                            'meta': current_meta,
                            'updated_at': int(time.time())
                        })
                        db.commit()  # Save to database
                        print(f"Updated model {model.name} with icon {new_icon}")
                    
                    return ModelModel.model_validate(model)
                return None
        except Exception:
            return None

    def toggle_model_by_id(self, id: str) -> Optional[ModelModel]:
        with get_db() as db:
            try:
                is_active = db.query(Model).filter_by(id=id).first().is_active

                db.query(Model).filter_by(id=id).update(
                    {
                        "is_active": not is_active,
                        "updated_at": int(time.time()),
                    }
                )
                db.commit()

                return self.get_model_by_id(id)
            except Exception:
                return None

    def update_model_by_id(self, id: str, model: ModelForm) -> Optional[ModelModel]:
        try:
            with get_db() as db:
                # update only the fields that are present in the model
                result = (
                    db.query(Model)
                    .filter_by(id=id)
                    .update(model.model_dump(exclude={"id"}))
                )
                db.commit()

                model = db.get(Model, id)
                db.refresh(model)
                return ModelModel.model_validate(model)
        except Exception as e:
            log.exception(f"Failed to update the model by id {id}: {e}")
            return None

    def delete_model_by_id(self, id: str) -> bool:
        try:
            with get_db() as db:
                db.query(Model).filter_by(id=id).delete()
                db.commit()

                return True
        except Exception:
            return False

    def delete_all_models(self) -> bool:
        try:
            with get_db() as db:
                db.query(Model).delete()
                db.commit()

                return True
        except Exception:
            return False


Models = ModelsTable()
