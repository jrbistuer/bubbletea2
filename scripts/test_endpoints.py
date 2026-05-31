"""End-to-end test of the BubbleTea CRUD endpoints using FastAPI's TestClient.

Runs against the real database configured in .env, so it will create and then
remove its own test row.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

BASE = "/bubbleteas"


def _check(condition: bool, message: str) -> None:
    status = "OK  " if condition else "FAIL"
    print(f"  [{status}] {message}")
    if not condition:
        raise SystemExit(1)


def main() -> int:
    print("Health check")
    r = client.get("/")
    _check(r.status_code == 200, f"GET / -> {r.status_code}")

    print("\nCreate")
    payload = {
        "name": "Test Taro",
        "temperature": "cold",
        "precio": 4.5,
        "active": True,
    }
    r = client.post(f"{BASE}/", json=payload)
    _check(r.status_code == 201, f"POST {BASE}/ -> {r.status_code}")
    created = r.json()
    _check("id" in created, f"created has id: {created}")
    item_id = created["id"]

    print("\nList")
    r = client.get(f"{BASE}/")
    _check(r.status_code == 200, f"GET {BASE}/ -> {r.status_code}")
    items = r.json()
    _check(any(i["id"] == item_id for i in items), "created item appears in list")

    print("\nGet by id")
    r = client.get(f"{BASE}/{item_id}")
    _check(r.status_code == 200, f"GET {BASE}/{item_id} -> {r.status_code}")
    _check(r.json()["name"] == "Test Taro", "name matches")

    print("\nUpdate")
    r = client.put(f"{BASE}/{item_id}", json={"precio": 5.25, "active": False})
    _check(r.status_code == 200, f"PUT {BASE}/{item_id} -> {r.status_code}")
    updated = r.json()
    _check(updated["precio"] == 5.25, f"precio updated -> {updated['precio']}")
    _check(updated["active"] is False, f"active updated -> {updated['active']}")

    print("\nGet missing (404)")
    r = client.get(f"{BASE}/999999999")
    _check(r.status_code == 404, f"GET missing -> {r.status_code}")

    print("\nDelete")
    r = client.delete(f"{BASE}/{item_id}")
    _check(r.status_code == 204, f"DELETE {BASE}/{item_id} -> {r.status_code}")

    print("\nGet after delete (404)")
    r = client.get(f"{BASE}/{item_id}")
    _check(r.status_code == 404, f"GET deleted -> {r.status_code}")

    print("\nAll endpoint tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
