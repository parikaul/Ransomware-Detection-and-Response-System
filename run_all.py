import subprocess, sys, threading
subprocess.Popen([sys.executable,"-m","app.main"])
subprocess.run([sys.executable,"-m","uvicorn","app.api.main:app","--host","0.0.0.0","--port","8000"])
