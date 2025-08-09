import re
import requests
from dataclasses import dataclass

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

@dataclass(frozen=True)
class RequestPayload:
    name: str
    email: str
    resource: str
    reason: str

    def validate(self):
        if not self.name.strip() or not self.email.strip() or not self.resource.strip() or not self.reason.strip():
            raise ValueError("All fields are required.")
        if not EMAIL_RE.match(self.email.strip().lower()):
            raise ValueError("Invalid email address.")

def send_request(
    payload: RequestPayload,
    request_api_url: str,
    http_post=requests.post,
    timeout: int = 10,
) -> dict:
    """
    Returns dict:
      {"action":"redirect","redirect_url":"..."} OR
      {"action":"message","ok":True/False,"message":"..."}
    """
    payload.validate()

    resp = http_post(
        request_api_url,
        json={
            "name": payload.name.strip(),
            "email": payload.email.strip().lower(),
            "resource": payload.resource.strip(),
            "reason": payload.reason.strip(),
        },
        allow_redirects=False,
        timeout=timeout,
    )

    # 30x redirect via Location header
    if resp.status_code in (301, 302, 303) and "Location" in resp.headers:
        return {"action": "redirect", "redirect_url": resp.headers["Location"]}

    # JSON contract fallback
    if resp.ok:
        try:
            data = resp.json()
        except Exception:
            return {"action": "message", "ok": False, "message": "Invalid JSON from server."}
        if data.get("action") == "redirect" and data.get("redirect_url"):
            return {"action": "redirect", "redirect_url": data["redirect_url"]}
        return {"action": "message", "ok": True, "message": data.get("message", "Request processed.")}

    snippet = resp.text[:200] if resp.text else ""
    return {"action": "message", "ok": False, "message": f"Request failed: {resp.status_code} {snippet}"}
