from collections import deque
from datetime import datetime, timedelta
from pathlib import Path
import shutil
import psutil
from app.detectors.scoring import score_signals
from app.database.models import Event, Score, Alert, Incident
from app.core.entropy import file_entropy

class DetectionEngine:
    def __init__(self, config, session, logger):
        self.cfg=config; self.session=session; self.logger=logger
        self.events=deque()
        self.last_incident=0

    def add_event(self, event):
        self.session.add(event); self.session.commit()
        self.events.append(event)
        cutoff=datetime.utcnow()-timedelta(seconds=self.cfg["window_seconds"])
        while self.events and self.events[0].timestamp < cutoff: self.events.popleft()
        return self.evaluate()

    def evaluate(self):
        ev=list(self.events)
        mods=sum(e.event_type in ("modify","create") for e in ev)
        renames=sum(e.event_type=="rename" for e in ev)
        ext_changes=sum(bool(e.old_extension and e.extension and e.old_extension != e.extension) for e in ev)
        ent=[e.entropy for e in ev if e.entropy]
        avg=sum(ent)/len(ent) if ent else 0
        t=self.cfg["thresholds"]
        signals={
          "rapid_encryption": mods >= t["modified_per_minute"],
          "mass_rename": renames >= t["renames"] or ext_changes >= t["extension_changes"],
          "high_entropy": avg >= t["average_entropy"],
          "cpu_spike": False,
          "unknown_program": False
        }
        score, level=score_signals(signals, self.cfg["weights"])
        self.session.add(Score(score=score, level=level)); self.session.commit()
        if level != "Normal":
            alert=Alert(score=score, level=level, message=f"Signals: {signals}")
            self.session.add(alert); self.session.commit()
            self.logger.warning(f"{level} alert score={score} signals={signals}")
        if level=="Critical" and self.last_incident != (ev[-1].id if ev else 0):
            affected=[e.path for e in ev if e.event_type in ("create","modify","rename")]
            q=Path(self.cfg["quarantine_dir"]); q.mkdir(parents=True, exist_ok=True)
            copied=[]
            for p in affected:
                src=Path(p)
                if src.exists() and src.is_file():
                    dest=q/src.name
                    try: shutil.copy2(src,dest); copied.append(str(dest))
                    except OSError: pass
            inc=Incident(score=score, level=level, affected_files="\n".join(affected), suspect_process="")
            self.session.add(inc); self.session.commit()
            self.last_incident=ev[-1].id if ev else 0
            self.logger.warning(f"INCIDENT score={score}; evidence_copied={len(copied)}")
            return {"score":score,"level":level,"signals":signals,"incident_id":inc.id}
        return {"score":score,"level":level,"signals":signals}
