from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import crud, models, schemas, auth, database, config, security
from .database import engine, get_db
import time

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title=config.settings.PROJECT_NAME)
app.add_middleware(security.RateLimitMiddleware, limit=60, window=60) # 60 rpm

@app.get("/")
def read_root():
    return {"message": "Welcome to TCOC API"}

@app.post("/users/me", response_model=schemas.UserSchema)
def get_or_create_user(db: Session = Depends(get_db), telegram_user: dict = Depends(auth.validate_telegram_data)):
    user = crud.get_user_by_telegram_id(db, telegram_id=str(telegram_user['id']))
    if not user:
        user = crud.create_user(db, schemas.UserCreate(
            telegram_id=str(telegram_user['id']),
            username=telegram_user.get('username')
        ))
    return user

@app.get("/users/me", response_model=schemas.UserSchema)
def read_user_me(db: Session = Depends(get_db), telegram_user: dict = Depends(auth.validate_telegram_data)):
    user = crud.get_user_by_telegram_id(db, telegram_id=str(telegram_user['id']))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/buildings/", response_model=schemas.BuildingSchema)
def create_building_for_user(building: schemas.BuildingCreate, db: Session = Depends(get_db), telegram_user: dict = Depends(auth.validate_telegram_data)):
    user = crud.get_user_by_telegram_id(db, telegram_id=str(telegram_user['id']))
    if user.gold < 500:
        raise HTTPException(status_code=400, detail="Not enough gold")
    user.gold -= 500
    return crud.create_building(db=db, building=building, user_id=user.id)

@app.post("/buildings/{building_id}/upgrade", response_model=schemas.BuildingSchema)
def upgrade_building(building_id: int, db: Session = Depends(get_db), telegram_user: dict = Depends(auth.validate_telegram_data)):
    user = crud.get_user_by_telegram_id(db, telegram_id=str(telegram_user['id']))
    building = db.query(models.Building).filter(models.Building.id == building_id, models.Building.user_id == user.id).first()
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    cost = building.level * 1000
    if user.gold < cost:
        raise HTTPException(status_code=400, detail="Not enough gold")
    user.gold -= cost
    return crud.upgrade_building(db=db, building_id=building_id)

@app.post("/units/train")
def train_units(unit_type: str, count: int, db: Session = Depends(get_db), telegram_user: dict = Depends(auth.validate_telegram_data)):
    user = crud.get_user_by_telegram_id(db, telegram_id=str(telegram_user['id']))
    cost = count * 50
    if user.gold < cost:
        raise HTTPException(status_code=400, detail="Not enough gold")
    user.gold -= cost
    unit = db.query(models.Unit).filter(models.Unit.user_id == user.id, models.Unit.type == unit_type).first()
    if not unit:
        unit = models.Unit(user_id=user.id, type=unit_type, count=count)
        db.add(unit)
    else:
        unit.count += count
    db.commit()
    return {"message": f"Trained {count} {unit_type}s", "current_count": unit.count}

@app.post("/battles/attack/{defender_id}")
def attack_player(defender_id: int, db: Session = Depends(get_db), telegram_user: dict = Depends(auth.validate_telegram_data)):
    from .game_logic import calculate_battle_result, regenerate_energy
    attacker = crud.get_user_by_telegram_id(db, telegram_id=str(telegram_user['id']))
    regenerate_energy(attacker)
    if attacker.energy < 10:
        raise HTTPException(status_code=400, detail="Not enough energy")
    defender = db.query(models.User).filter(models.User.id == defender_id).first()
    if not defender:
        raise HTTPException(status_code=404, detail="Defender not found")
    attacker.energy -= 10
    result = calculate_battle_result(attacker, defender)
    battle = models.Battle(attacker_id=attacker.id, defender_id=defender.id, result=result, gold_looted=result['gold_looted'], was_win=result['was_win'])
    db.add(battle)
    if result['was_win']:
        attacker.rank += 10
    else:
        attacker.rank = max(0, attacker.rank - 5)
    db.commit()
    return result

@app.get("/leaderboard", response_model=List[schemas.UserSchema])
def get_leaderboard(db: Session = Depends(get_db)):
    return db.query(models.User).order_by(models.User.rank.desc()).limit(10).all()

@app.post("/clans/", response_model=schemas.ClanSchema)
def create_clan(clan: schemas.ClanCreate, db: Session = Depends(get_db), telegram_user: dict = Depends(auth.validate_telegram_data)):
    user = crud.get_user_by_telegram_id(db, telegram_id=str(telegram_user['id']))
    if user.clan_id:
        raise HTTPException(status_code=400, detail="Already in a clan")
    db_clan = models.Clan(name=clan.name, description=clan.description, leader_id=user.id)
    db.add(db_clan)
    db.commit()
    db.refresh(db_clan)
    user.clan_id = db_clan.id
    db.commit()
    return db_clan

@app.post("/wallet/connect")
def connect_wallet(address: str, db: Session = Depends(get_db), telegram_user: dict = Depends(auth.validate_telegram_data)):
    user = crud.get_user_by_telegram_id(db, telegram_id=str(telegram_user['id']))
    user.ton_wallet = address
    db.commit()
    return {"message": "Wallet connected", "address": address}

@app.post("/nfts/mint")
def mint_nft(nft_type: str, db: Session = Depends(get_db), telegram_user: dict = Depends(auth.validate_telegram_data)):
    user = crud.get_user_by_telegram_id(db, telegram_id=str(telegram_user['id']))
    if not user.ton_wallet:
        raise HTTPException(status_code=400, detail="Connect wallet first")
    nft = models.NFT(user_id=user.id, nft_address=f"EQ_{hash(str(user.id) + str(time.time()))}", type=nft_type, metadata_url=f"https://api.tcoc.game/nfts/{nft_type}.json")
    db.add(nft)
    db.commit()
    return {"message": "NFT minting triggered", "nft_address": nft.nft_address}
