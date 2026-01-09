# backend/api/schemas/license.py
from pydantic import BaseModel, ConfigDict
from datetime import datetime

# -------------------
# License base
# -------------------
class LicenseBase(BaseModel):
    name: str
    description: str | None = None
    expires_at: datetime

# -------------------
# Criar licença (input)
# -------------------
class LicenseCreate(LicenseBase):
    pass

# -------------------
# Atualizar licença (input)
# -------------------
class LicenseUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    expires_at: datetime | None = None

# -------------------
# Leitura da licença (output)
# -------------------
class LicenseRead(LicenseBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
