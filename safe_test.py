import os, pathlib
sandbox=pathlib.Path("data/sandbox"); sandbox.mkdir(parents=True,exist_ok=True)
for i in range(25): (sandbox/f"file_{i}.txt").write_text("normal document content")
for f in list(sandbox.glob("*.txt")):
    f.write_bytes(os.urandom(20000))
    f.rename(f.with_suffix(".locked"))
print("SAFE TEST COMPLETE: created/overwrote/renamed only files under data/sandbox")
