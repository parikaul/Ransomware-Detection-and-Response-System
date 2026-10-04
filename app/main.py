import argparse, time, psutil
from app.core.config import load_config
from app.core.logging import setup_logging
from app.database.models import get_session, ProcessSnapshot
from app.detectors.engine import DetectionEngine
from app.detectors.file_monitor import start_monitor

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--watch", default=None)
    args=ap.parse_args()
    cfg=load_config(); logger=setup_logging(); session=get_session(cfg["database_url"])
    engine=DetectionEngine(cfg, session, logger)
    watch=args.watch or cfg["watch_paths"][0]
    obs=start_monitor(watch,engine)
    try:
        while True:
            for p in psutil.process_iter(["pid","name","cpu_percent","memory_percent","exe","ppid"]):
                try:
                    i=p.info; session.add(ProcessSnapshot(pid=i["pid"],name=i.get("name") or "",cpu_percent=i.get("cpu_percent") or 0,memory_percent=i.get("memory_percent") or 0,exe=i.get("exe") or "",parent_pid=i.get("ppid") or 0))
                except (psutil.NoSuchProcess, psutil.AccessDenied): pass
            session.commit()
            time.sleep(5)
    except KeyboardInterrupt:
        obs.stop(); obs.join(); print("Monitor stopped.")

if __name__=="__main__": main()
