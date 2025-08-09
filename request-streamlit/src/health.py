import os
from flask import Flask

app = Flask(__name__)

@app.get("/health")
def health():
    return "OK", 200

@app.get("/ready")
def ready():
    return "READY", 200

if __name__ == "__main__":
    port = int(os.getenv("HEALTH_PORT", "8080"))
    print(f"[health] Starting Flask health server on 0.0.0.0:{port}", flush=True)
    app.run(host="0.0.0.0", port=port)
