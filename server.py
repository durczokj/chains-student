"""
Adapter: a Flask server that proxies the student-facing API
to the Django chains backend.

The test script (test_api.py) calls this server on port 5050.
Your job is to implement each route so that it correctly forwards
requests to the backend and returns the responses.

Run:
    1. docker compose up
    2. docker compose exec app python test_api.py
    3. Edit this file, then: docker compose restart

Repeat steps 2–3 until all tests pass.
"""

import requests
from flask import Flask, Response, jsonify, request

app = Flask(__name__)

# ── Configuration ─────────────────────────────────────────────────────

# TODO: Set the backend URL
DJANGO_URL = "..."

# Reference data that must be seeded during setup
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


# ── Helpers ───────────────────────────────────────────────────────────
# TIP: You may want to create helper functions to avoid repeating
# the same requests.get / requests.post / requests.delete logic
# in every route. Think about what parameters they need and what
# they should return (hint: look at Flask's Response class).


# ── Setup ─────────────────────────────────────────────────────────────

@app.route("/api/setup/", methods=["POST"])
def setup():
    """
    Reset state and seed reference data in the Django backend.

    This endpoint should:
    1. Delete ALL existing events (fetch pages of events and delete each one)
    2. Ensure all COUNTRIES exist (check if each exists, create if not)
    3. Ensure all CODE_TYPES exist (check if each exists, create if not)

    Backend API reference:
      - GET  /api/events/?page_size=100  → paginated list (check "results" key)
      - DELETE /api/events/<id>/
      - GET  /api/countries/<code>/       → 404 if missing
      - POST /api/countries/              → {"code": ..., "name": ...}
      - GET  /api/code-types/<id>/        → 404 if missing
      - POST /api/code-types/             → {"id": ..., "type": ...}

    Return: jsonify({"status": "ok"}), 200
    """
    # TODO: Implement setup logic
    pass


# ── Events ────────────────────────────────────────────────────────────

@app.route("/api/events/", methods=["GET"])
def list_events():
    """
    List events. Forward query parameters (e.g. page_size) to the backend.
    Backend: GET /api/events/
    """
    # TODO: Implement
    pass


@app.route("/api/events/", methods=["POST"])
def create_event():
    """
    Create a new event. Forward the JSON body to the backend.
    Backend: POST /api/events/
    """
    # TODO: Implement
    pass


@app.route("/api/events/<int:event_id>/", methods=["GET"])
def get_event(event_id):
    """
    Get a single event by ID.
    Backend: GET /api/events/<event_id>/
    """
    # TODO: Implement
    pass


@app.route("/api/events/<int:event_id>/", methods=["DELETE"])
def delete_event(event_id):
    """
    Delete a single event by ID.
    Backend: DELETE /api/events/<event_id>/
    """
    # TODO: Implement
    pass


# ── Product Families ─────────────────────────────────────────────────

@app.route("/api/product-families/", methods=["GET"])
def list_families():
    """
    List product families. Forward query parameters to the backend.
    Backend: GET /api/product-families/
    """
    # TODO: Implement
    pass


@app.route("/api/product-families/<int:family_id>/", methods=["GET"])
def get_family(family_id):
    """
    Get a single product family by ID.
    Backend: GET /api/product-families/<family_id>/
    """
    # TODO: Implement
    pass


@app.route("/api/product-families/recompute/", methods=["POST"])
def recompute():
    """
    Trigger family recomputation. Forward the JSON body to the backend.
    Backend: POST /api/product-families/recompute/
    """
    # TODO: Implement
    pass


# ── Resolution ───────────────────────────────────────────────────────

@app.route("/api/resolve/", methods=["GET"])
def resolve():
    """
    Resolve a code to its product family. Forward query parameters.
    Backend: GET /api/resolve/
    """
    # TODO: Implement
    pass


@app.route("/api/resolve/reverse/", methods=["GET"])
def resolve_reverse():
    """
    Reverse-resolve a family identifier to its codes. Forward query parameters.
    Backend: GET /api/resolve/reverse/
    """
    # TODO: Implement
    pass


@app.route("/api/resolve/bulk/", methods=["POST"])
def resolve_bulk():
    """
    Bulk-resolve codes. Forward the JSON body to the backend.
    Backend: POST /api/resolve/bulk/
    """
    # TODO: Implement
    pass


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
