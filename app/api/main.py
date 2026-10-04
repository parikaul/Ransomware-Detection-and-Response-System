from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.core.config import load_config
from app.database.models import get_session, Event, Alert, Incident, Score

app=FastAPI(title="RDRS API", version="1.0")
cfg=load_config()

@app.get("/health")
def health(): return {"status":"ok","simulation_mode":cfg["simulation_mode"]}

@app.get("/status")
def status():
    s=get_session(cfg["database_url"])
    try:
        x=s.query(Score).order_by(Score.timestamp.desc()).first()
        return {"level": x.level if x else "Normal", "score": x.score if x else 0}
    finally: s.close()

@app.get("/alerts")
def alerts():
    s=get_session(cfg["database_url"])
    try:
        return [{"id":x.id,"score":x.score,"level":x.level,"message":x.message,"timestamp":x.timestamp.isoformat()}
                for x in s.query(Alert).order_by(Alert.timestamp.desc()).limit(50)]
    finally: s.close()

@app.get("/events")
def events():
    s=get_session(cfg["database_url"])
    try:
        return [{"id":x.id,"type":x.event_type,"path":x.path,"entropy":x.entropy,"timestamp":x.timestamp.isoformat()}
                for x in s.query(Event).order_by(Event.timestamp.desc()).limit(100)]
    finally: s.close()

@app.get("/reports")
def reports():
    s=get_session(cfg["database_url"])
    try:
        return [{"id":x.id,"score":x.score,"level":x.level,"created_at":x.created_at.isoformat()}
                for x in s.query(Incident).order_by(Incident.created_at.desc()).limit(50)]
    finally: s.close()

@app.post("/scan")
def scan():
    return {"status":"accepted","message":"Manual scan request recorded; use the file monitor for real-time analysis."}

@app.post("/settings")
def settings(payload: dict):
    allowed={"window_seconds","thresholds","weights","simulation_mode"}
    changed={k:v for k,v in payload.items() if k in allowed}
    cfg.update(changed)
    return {"status":"updated","settings":changed}

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    return Path("app/dashboard/index.html").read_text(encoding="utf-8")
