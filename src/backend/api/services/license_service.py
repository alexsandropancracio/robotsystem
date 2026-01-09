# backend/api/services/license_service.py
from sqlalchemy.orm import Session
from typing import List, Optional

from backend.api.repositories.license_repository import LicenseRepository
from backend.api.schemas.license import LicenseCreate, LicenseUpdate, LicenseRead

repo = LicenseRepository()

def create_license_service(db: Session, license_in: LicenseCreate) -> LicenseRead:
    license_obj = repo.create(db, license_in)
    return LicenseRead.from_orm(license_obj)

def list_licenses_service(db: Session) -> List[LicenseRead]:
    licenses = repo.get_all(db)
    return [LicenseRead.from_orm(l) for l in licenses]

def get_license_service(db: Session, license_id: int) -> Optional[LicenseRead]:
    license_obj = repo.get(db, license_id)
    if not license_obj:
        return None
    return LicenseRead.from_orm(license_obj)

def update_license_service(db: Session, license_id: int, license_in: LicenseUpdate) -> Optional[LicenseRead]:
    license_obj = repo.get(db, license_id)
    if not license_obj:
        return None
    updated_obj = repo.update(db, license_obj, **license_in.dict())
    return LicenseRead.from_orm(updated_obj)

def delete_license_service(db: Session, license_id: int) -> bool:
    license_obj = repo.get(db, license_id)
    if not license_obj:
        return False
    repo.delete(db, license_obj)
    return True
