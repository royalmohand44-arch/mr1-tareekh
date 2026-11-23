import subprocess,json
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
class H(SimpleHTTPRequestHandler):
 def __init__(s,*a,**k): super().__init__(*a,directory="playground",**k)
 def do_POST(s):
  c=json.loads(s.rfile.read(int(s.headers["Content-Length"])))["code"]
  try:
   r=subprocess.run(["python3","-c",c],capture_output=True,text=True,timeout=8)
   out=r.stdout if r.returncode==0 else r.stderr
  except Exception as e: out=str(e)
  s.send_response(200);s.send_header("Content-Type","application/json");s.end_headers()
  s.wfile.write(json.dumps({"output":out or "✅ تم التنفيذ بنجاح"}).encode())
print("READY 8080");ThreadingHTTPServer(("0.0.0.0",8080),H).serve_forever()