import csv, json
from pathlib import Path
from app.core.config import load_config
from app.database.models import get_session, Incident, Event
def generate():
    cfg=load_config(); s=get_session(cfg["database_url"]); out=Path("reports"); out.mkdir(exist_ok=True)
    inc=s.query(Incident).order_by(Incident.created_at.desc()).first()
    if not inc: raise SystemExit("No incident found.")
    events=s.query(Event).order_by(Event.timestamp).all()
    data={"incident_id":inc.id,"score":inc.score,"level":inc.level,"affected_files":inc.affected_files.splitlines(),"suspect_process":inc.suspect_process,"timeline":[{"type":e.event_type,"path":e.path,"entropy":e.entropy,"timestamp":e.timestamp.isoformat()} for e in events]}
    (out/"incident.json").write_text(json.dumps(data,indent=2),encoding="utf-8")
    with open(out/"incident.csv","w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(["timestamp","event_type","path","entropy"])
        for e in events: w.writerow([e.timestamp.isoformat(),e.event_type,e.path,e.entropy])
    print("Generated reports/incident.json and reports/incident.csv")
if __name__=="__main__": generate()
