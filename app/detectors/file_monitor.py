from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from app.database.models import Event
from app.core.entropy import file_entropy

class Handler(FileSystemEventHandler):
    def __init__(self, engine):
        self.engine=engine
    def _add(self, typ, path, old=""):
        p=Path(path); ent=0.0
        if typ in ("create","modify") and p.is_file():
            try: ent=file_entropy(p, self.engine.cfg["entropy_sample_bytes"])
            except OSError: pass
        ev=Event(event_type=typ,path=str(p),extension=p.suffix,old_extension=old,entropy=ent)
        result=self.engine.add_event(ev)
        print(f"[EVENT] {typ:6} {p} entropy={ent:.2f} -> {result['level']} {result['score']}")
    def on_created(self,e):
        if not e.is_directory: self._add("create",e.src_path)
    def on_modified(self,e):
        if not e.is_directory: self._add("modify",e.src_path)
    def on_deleted(self,e):
        if not e.is_directory: self._add("delete",e.src_path)
    def on_moved(self,e):
        if not e.is_directory:
            self._add("rename",e.dest_path,Path(e.src_path).suffix)

def start_monitor(path, engine):
    obs=Observer(); obs.schedule(Handler(engine), str(path), recursive=True); obs.start()
    print(f"Monitoring: {Path(path).resolve()}")
    return obs
