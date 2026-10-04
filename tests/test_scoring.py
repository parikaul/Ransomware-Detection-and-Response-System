from app.detectors.scoring import score_signals
def test_critical():
    s,l=score_signals({"rapid_encryption":True,"mass_rename":True,"high_entropy":True},{"rapid_encryption":40,"mass_rename":30,"high_entropy":25})
    assert s==95 and l=="Critical"
def test_normal():
    s,l=score_signals({"rapid_encryption":False},{"rapid_encryption":40})
    assert s==0 and l=="Normal"
