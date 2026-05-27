from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ProfileCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=15,
        description="Nome de exibição do perfil (ex: Ítalo, Infantil)"
    )
    avatar_asset_path: str = Field(
        ...,
        description="Caminho do asset local configurado no pubspec.yaml do Flutter"
    )
    device_id: str = Field(
        ...,
        description="ID único do dispositivo físico capturado pelo device_info_plus"
    )
    device_name: Optional[str] = Field(
        "Dispositivo Não Identificado",
        description="Nome ou modelo do aparelho (ex: Samsung S24, iPhone 15)"
    )
    
class DeviceInfoSchema(BaseModel):
    device_id: str
    device_name: str
    last_login: str

class ProfileResponse(BaseModel):
    id: str
    account_id: str
    name: str
    avatar_asset_path: str
    active_devices: List[DeviceInfoSchema]

    class Config:
        from_attributes = True