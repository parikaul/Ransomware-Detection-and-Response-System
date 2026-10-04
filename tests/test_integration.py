from app.core.config import load_config
from app.database.models import init_db, get_session, Event
from app.detectors.engine import DetectionEngine
from app.core.logging import setup_logging
def test_burst(tmp_path):
    cfg=load_config(str(__import__("pathlib").Path(__file__).parents[1]/"config.yaml"))
    db=f"sqlite:///{tmp_path/'t.db'}"; init_db(db); s=get_session(db)
    cfg["quarantine_dir"]=str(tmp_path/"q"); e=DetectionEngine(cfg,s,setup_logging(str(tmp_path/"logs")))
    for i in range(25):
        e.add_event(Event(event_type="modify",path=str(tmp_path/f"{i}.txt"),extension=".txt",entropy=7.8))
    for i in range(10):
        e.add_event(Event(event_type="rename",path=str(tmp_path/f"{i}.locked"),extension=".locked",old_extension=".txt",entropy=7.8))
    assert e.evaluate()["level"]=="Critical"
