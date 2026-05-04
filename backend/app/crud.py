from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime, timedelta

def get_user_by_telegram_id(db: Session, telegram_id: str):
    return db.query(models.User).filter(models.User.telegram_id == telegram_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(telegram_id=user.telegram_id, username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_buildings(db: Session, user_id: int):
    return db.query(models.Building).filter(models.Building.user_id == user_id).all()

def create_building(db: Session, building: schemas.BuildingCreate, user_id: int):
    db_building = models.Building(**building.dict(), user_id=user_id)
    db.add(db_building)
    db.commit()
    db.refresh(db_building)
    return db_building

def upgrade_building(db: Session, building_id: int):
    db_building = db.query(models.Building).filter(models.Building.id == building_id).first()
    if db_building:
        duration = db_building.level * 5
        db_building.upgrade_end_time = datetime.utcnow() + timedelta(minutes=duration)
        db.commit()
        db.refresh(db_building)
    return db_building
