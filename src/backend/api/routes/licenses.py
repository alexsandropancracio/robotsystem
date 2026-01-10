# backend/api/routes/licenses.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from backend.api.schemas.license import LicenseCreate, LicenseRead, LicenseUpdate
from backend.api.services import license_service
from backend.api.deps.database import get_db
from backend.api.core.auth import get_current_user
from backend.api.models.user import User
from backend.api.deps.admin import require_admin


router = APIRouter(
    prefix="/licenses",
    tags=["Licenses"],
)

# -------------------
# Criar licença
# -------------------
@router.post("/", response_model=LicenseRead, status_code=status.HTTP_201_CREATED)
def create_license(
    license_in: LicenseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),

):
    return license_service.create_license_service(db, license_in)

# -------------------
# Listar licenças
# -------------------
@router.get("/", response_model=List[LicenseRead])
def list_licenses(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return license_service.list_licenses_service(db)

# -------------------
# Buscar licença por ID
# -------------------
@router.get("/{license_id}", response_model=LicenseRead)
def get_license(license_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    license_obj = license_service.get_license_service(db, license_id)
    if not license_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="License not found")
    return license_obj

# -------------------
# Atualizar licença
# -------------------
@router.put("/{license_id}", response_model=LicenseRead)
def update_license(license_id: int, license_in: LicenseUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    updated = license_service.update_license_service(db, license_id, license_in)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="License not found")
    return updated

# -------------------
# Deletar licença
# -------------------
@router.delete("/{license_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_license(license_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    deleted = license_service.delete_license_service(db, license_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="License not found")
