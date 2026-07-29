"""
Example adapter: a Flask server that proxies the student-facing API
to the Django chains backend.

The test script calls this server on port 5050.
This server translates requests and forwards them to the Django app.

Run:
    1. export CHAINS_USERNAME=... CHAINS_PASSWORD=...
    2. python server_example.py
    3. In another terminal: python ../test_api.py

Configuration (all via env vars):
    CHAINS_URL       backend base URL (default: https://chains.durczok.ovh)
    CHAINS_USERNAME  HTTP Basic auth username
    CHAINS_PASSWORD  HTTP Basic auth password
"""

import os

import requests
from flask import Flask, Response, jsonify, request

app = Flask(__name__)

# ── Backend configuration ─────────────────────────────────────────────
# The chains backend requires HTTP Basic authentication on every request.
# Credentials will be provided to you separately — do not commit them to git.
DJANGO_URL = os.environ.get("CHAINS_URL", "https://chains.durczok.ovh").rstrip("/")
CHAINS_USERNAME = os.environ.get("CHAINS_USERNAME", "")
CHAINS_PASSWORD = os.environ.get("CHAINS_PASSWORD", "")

# One shared Session — attach auth once, reuse the TCP connection.
BACKEND = requests.Session()
if CHAINS_USERNAME and CHAINS_PASSWORD:
    BACKEND.auth = (CHAINS_USERNAME, CHAINS_PASSWORD)

COUNTRIES = [
    ("PL", "Poland"),
    ("DE", "Germany"),
    ("US", "United States"),
    ("JP", "Japan"),
    ("CN", "China"),
]

CODE_TYPES = [
    ("IPC", "Internal Product Code"),
    ("GTIN", "Global Trade Item Number"),
]


def _proxy_get(path: str, params: dict | None = None) -> Response:
    r = BACKEND.get(f"{DJANGO_URL}{path}", params=params)
    return Response(r.content, status=r.status_code, content_type=r.headers.get("Content-Type", "application/json"))


def _proxy_post(path: str, data: dict | None = None) -> Response:
    r = BACKEND.post(f"{DJANGO_URL}{path}", json=data)
    return Response(r.content, status=r.status_code, content_type=r.headers.get("Content-Type", "application/json"))


def _proxy_delete(path: str) -> Response:
    r = BACKEND.delete(f"{DJANGO_URL}{path}")
    return Response(r.content, status=r.status_code, content_type=r.headers.get("Content-Type", "application/json"))


# ── Setup ─────────────────────────────────────────────────────────────

@app.route("/api/setup/", methods=["POST"])
def setup():
    """Reset state and seed countries and code types in the Django backend."""
    # Delete all existing events
    while True:
        r = BACKEND.get(f"{DJANGO_URL}/api/events/", params={"page_size": 100})
        if r.status_code != 200:
            break
        data = r.json()
        events = data.get("results", data) if isinstance(data, dict) else data
        if not events:
            break
        for ev in events:
            BACKEND.delete(f"{DJANGO_URL}/api/events/{ev['id']}/")

    # Ensure countries exist
    for code, name in COUNTRIES:
        r = BACKEND.get(f"{DJANGO_URL}/api/countries/{code}/")
        if r.status_code == 404:
            BACKEND.post(f"{DJANGO_URL}/api/countries/", json={"code": code, "name": name})

    # Ensure code types exist
    for ct_id, ct_type in CODE_TYPES:
        r = BACKEND.get(f"{DJANGO_URL}/api/code-types/{ct_id}/")
        if r.status_code == 404:
            BACKEND.post(f"{DJANGO_URL}/api/code-types/", json={"id": ct_id, "type": ct_type})

    return jsonify({"status": "ok"}), 200


# ── Events (pass-through) ────────────────────────────────────────────

@app.route("/api/events/", methods=["GET"])
def list_events():
    return _proxy_get("/api/events/", dict(request.args))


@app.route("/api/events/", methods=["POST"])
def create_event():
    return _proxy_post("/api/events/", request.get_json())


@app.route("/api/events/<int:event_id>/", methods=["GET"])
def get_event(event_id):
    return _proxy_get(f"/api/events/{event_id}/")


@app.route("/api/events/<int:event_id>/", methods=["DELETE"])
def delete_event(event_id):
    return _proxy_delete(f"/api/events/{event_id}/")


# ── Product Families (pass-through) ──────────────────────────────────

@app.route("/api/product-families/", methods=["GET"])
def list_families():
    return _proxy_get("/api/product-families/", dict(request.args))


@app.route("/api/product-families/<int:family_id>/", methods=["GET"])
def get_family(family_id):
    return _proxy_get(f"/api/product-families/{family_id}/")


@app.route("/api/product-families/recompute/", methods=["POST"])
def recompute():
    return _proxy_post("/api/product-families/recompute/", request.get_json())


# ── Resolution (pass-through) ────────────────────────────────────────

@app.route("/api/resolve/", methods=["GET"])
def resolve():
    return _proxy_get("/api/resolve/", dict(request.args))


@app.route("/api/resolve/reverse/", methods=["GET"])
def resolve_reverse():
    return _proxy_get("/api/resolve/reverse/", dict(request.args))


@app.route("/api/resolve/bulk/", methods=["POST"])
def resolve_bulk():
    return _proxy_post("/api/resolve/bulk/", request.get_json())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
