from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String, unique=True, index=True)
    username = Column(String, nullable=True)
    gold = Column(Float, default=1000.0)
    energy = Column(Float, default=100.0)
    max_energy = Column(Float, default=100.0)
    last_energy_regen = Column(DateTime(timezone=True), server_default=func.now())
    ton_wallet = Column(String, nullable=True)
    rank = Column(Integer, default=0)
    clan_id = Column(Integer, ForeignKey("clans.id"), nullable=True)

    buildings = relationship("Building", back_populates="owner")
    units = relationship("Unit", back_populates="owner")
    clan = relationship("Clan", back_populates="members")
    nfts = relationship("NFT", back_populates="owner")
    quest_progress = relationship("QuestProgress", back_populates="user")

class Building(Base):
    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(String)  # e.g., "town_hall", "gold_mine", "cannon"
    level = Column(Integer, default=1)
    x = Column(Integer)
    y = Column(Integer)
    upgrade_end_time = Column(DateTime(timezone=True), nullable=True)

    owner = relationship("User", back_populates="buildings")

class Unit(Base):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(String)  # e.g., "warrior", "archer"
    level = Column(Integer, default=1)
    count = Column(Integer, default=0)

    owner = relationship("User", back_populates="units")

class Clan(Base):
    __tablename__ = "clans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)
    leader_id = Column(Integer, ForeignKey("users.id"))

    members = relationship("User", back_populates="clan")
    wars = relationship("ClanWar", primaryjoin="or_(Clan.id==ClanWar.clan1_id, Clan.id==ClanWar.clan2_id)")

class ClanWar(Base):
    __tablename__ = "clan_wars"

    id = Column(Integer, primary_key=True, index=True)
    clan1_id = Column(Integer, ForeignKey("clans.id"))
    clan2_id = Column(Integer, ForeignKey("clans.id"))
    start_time = Column(DateTime(timezone=True))
    end_time = Column(DateTime(timezone=True))
    clan1_score = Column(Integer, default=0)
    clan2_score = Column(Integer, default=0)
    status = Column(String)  # "active", "completed"

class Battle(Base):
    __tablename__ = "battles"

    id = Column(Integer, primary_key=True, index=True)
    attacker_id = Column(Integer, ForeignKey("users.id"))
    defender_id = Column(Integer, ForeignKey("users.id"))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    result = Column(JSON)  # Store details about units lost, buildings destroyed
    gold_looted = Column(Float)
    was_win = Column(Boolean)

class NFT(Base):
    __tablename__ = "nfts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    nft_address = Column(String, unique=True, index=True)
    metadata_url = Column(String)
    type = Column(String)  # "hero", "skin", "item"
    stats = Column(JSON)

    owner = relationship("User", back_populates="nfts")

class Quest(Base):
    __tablename__ = "quests"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    target_count = Column(Integer)
    quest_type = Column(String) # "attack", "train", "upgrade"
    reward_gold = Column(Float)

class QuestProgress(Base):
    __tablename__ = "quest_progress"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    quest_id = Column(Integer, ForeignKey("quests.id"))
    current_count = Column(Integer, default=0)
    completed = Column(Boolean, default=False)

    user = relationship("User", back_populates="quest_progress")
    quest = relationship("Quest")
