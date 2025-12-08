import time
from typing import Optional
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Column, String, Float, BigInteger, ForeignKey
from sqlalchemy.orm import relationship
from open_webui.internal.db import Base, get_db
from open_webui.models.users import Users

class VirtualKey(Base):
    __tablename__ = "virtual_key"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("user.id"), nullable=False)
    key_hash = Column(String, unique=True, nullable=False)
    key_name = Column(String)
    budget_limit = Column(Float, default=0.0)
    spend_current = Column(Float, default=0.0)
    created_at = Column(BigInteger)
    updated_at = Column(BigInteger)

    user = relationship("User", back_populates="virtual_keys")

class VirtualKeyModel(BaseModel):
    id: str
    user_id: str
    key_name: str
    budget_limit: float
    spend_current: float
    created_at: int
    updated_at: int

    model_config = ConfigDict(from_attributes=True)

class CreateVirtualKeyForm(BaseModel):
    user_id: str
    key_name: str
    budget_limit: float = 10.0

class VirtualKeysTable:
    def insert_new_key(self, id: str, user_id: str, key_hash: str, key_name: str, budget_limit: float) -> Optional[VirtualKeyModel]:
        actual_user = Users.get_user_by_id(user_id)
        with get_db() as db:
            key = VirtualKey(
                id=id,
                user_id=user_id,
                key_hash=key_hash,
                key_name=key_name,
                budget_limit=budget_limit,
                spend_current=0.0,
                created_at=int(time.time()),
                updated_at=int(time.time()),
                user=actual_user
            )
            db.add(key)
            db.commit()
            db.refresh(key)
            return VirtualKeyModel.model_validate(key)

    def get_key_by_hash(self, key_hash: str) -> Optional[VirtualKeyModel]:
        with get_db() as db:
            key = db.query(VirtualKey).filter_by(key_hash=key_hash).first()
            if key:
                return VirtualKeyModel.model_validate(key)
            return None

    def update_spend(self, id: str, amount: float):
        with get_db() as db:
            key = db.query(VirtualKey).filter_by(id=id).first()
            if key:
                key.spend_current += amount
                key.updated_at = int(time.time())
                db.commit()

VirtualKeys = VirtualKeysTable()

