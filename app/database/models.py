from datetime import datetime
from sqlalchemy import create_engine, String, Integer, Float, Boolean, DateTime, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

class Base(DeclarativeBase): pass

class Event(Base):
    __tablename__="events"
    id: Mapped[int]=mapped_column(Integer, primary_key=True)
    event_type: Mapped[str]=mapped_column(String(20))
    path: Mapped[str]=mapped_column(Text)
    extension: Mapped[str]=mapped_column(String(50), default="")
    old_extension: Mapped[str]=mapped_column(String(50), default="")
    entropy: Mapped[float]=mapped_column(Float, default=0.0)
    timestamp: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow)

class ProcessSnapshot(Base):
    __tablename__="processes"
    id: Mapped[int]=mapped_column(Integer, primary_key=True)
    pid: Mapped[int]=mapped_column(Integer)
    name: Mapped[str]=mapped_column(String(255), default="")
    cpu_percent: Mapped[float]=mapped_column(Float, default=0.0)
    memory_percent: Mapped[float]=mapped_column(Float, default=0.0)
    exe: Mapped[str]=mapped_column(Text, default="")
    parent_pid: Mapped[int]=mapped_column(Integer, default=0)
    timestamp: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow)

class Score(Base):
    __tablename__="scores"
    id: Mapped[int]=mapped_column(Integer, primary_key=True)
    score: Mapped[float]=mapped_column(Float)
    level: Mapped[str]=mapped_column(String(20))
    timestamp: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow)

class Alert(Base):
    __tablename__="alerts"
    id: Mapped[int]=mapped_column(Integer, primary_key=True)
    score: Mapped[float]=mapped_column(Float)
    level: Mapped[str]=mapped_column(String(20))
    message: Mapped[str]=mapped_column(Text)
    timestamp: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow)

class Incident(Base):
    __tablename__="incidents"
    id: Mapped[int]=mapped_column(Integer, primary_key=True)
    score: Mapped[float]=mapped_column(Float)
    level: Mapped[str]=mapped_column(String(20))
    affected_files: Mapped[str]=mapped_column(Text)
    suspect_process: Mapped[str]=mapped_column(Text, default="")
    created_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.utcnow)

def init_db(url="sqlite:///./data/rdrs.db"):
    engine=create_engine(url, future=True)
    Base.metadata.create_all(engine)
    return engine

def get_session(url="sqlite:///./data/rdrs.db"):
    engine=init_db(url)
    return sessionmaker(bind=engine)()
