import types
import pytest
from src.logic import RequestPayload, send_request

def _resp(status=200, json_data=None, headers=None, text=""):
    r = types.SimpleNamespace()
    r.status_code = status
    r.headers = headers or {}
    r.text = text
    r.ok = 200 <= status < 300
    def _json():
        if json_data is None:
            raise ValueError("no json")
        return json_data
    r.json = _json
    return r

def test_validation_errors():
    with pytest.raises(ValueError):
        RequestPayload(name="", email="a@b.com", resource="r", reason="z").validate()
    with pytest.raises(ValueError):
        RequestPayload(name="a", email="bad", resource="r", reason="z").validate()

def test_redirect_via_location_header():
    payload = RequestPayload("A", "a@example.com", "r", "z")
    def fake_post(url, **kwargs):
        return _resp(status=303, headers={"Location": "https://success/page"})
    res = send_request(payload, "http://api/requests", http_post=fake_post)
    assert res["action"] == "redirect"
    assert res["redirect_url"] == "https://success/page"

def test_redirect_via_json():
    payload = RequestPayload("A", "a@example.com", "r", "z")
    def fake_post(url, **kwargs):
        return _resp(json_data={"action":"redirect","redirect_url":"https://ok"})
    res = send_request(payload, "http://api/requests", http_post=fake_post)
    assert res["action"] == "redirect"
    assert res["redirect_url"] == "https://ok"

def test_message_success():
    payload = RequestPayload("A", "a@example.com", "r", "z")
    def fake_post(url, **kwargs):
        return _resp(json_data={"message":"done"})
    res = send_request(payload, "http://api/requests", http_post=fake_post)
    assert res["action"] == "message"
    assert res["ok"] is True
    assert "done" in res["message"]

def test_message_failure():
    payload = RequestPayload("A", "a@example.com", "r", "z")
    def fake_post(url, **kwargs):
        return _resp(status=500, text="boom")
    res = send_request(payload, "http://api/requests", http_post=fake_post)
    assert res["action"] == "message"
    assert res["ok"] is False
    assert "500" in res["message"]
