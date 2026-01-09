# backend/api/repositories/license_repository.py
from sqlalchemy.orm import Session
from typing import Optional, List

from backend.api.models.license import License
from backend.api.schemas.license import LicenseCreate

class LicenseRepository:
    """
    Repositório CRUD para Licenses
    """

    def create(self, db: Session, license_in: LicenseCreate) -> License:
        license_obj = License(
            name=license_in.name,
            description=license_in.description,
            expires_at=license_in.expires_at,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(license_obj)
        db.commit()
        db.refresh(license_obj)
        return license_obj

    def get(self, db: Session, license_id: int) -> Optional[License]:
        return db.query(License).filter(License.id == license_id).first()

    def get_all(self, db: Session) -> List[License]:
        return db.query(License).all()

    def update(self, db: Session, license_obj: License, **kwargs) -> License:
        for attr, value in kwargs.items():
            if value is not None:
                setattr(license_obj, attr, value)
        license_obj.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(license_obj)
        return license_obj

    def delete(self, db: Session, license_obj: License) -> None:
        db.delete(license_obj)
        db.commit()
