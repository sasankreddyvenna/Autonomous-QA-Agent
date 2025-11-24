# backend/tests/test_routes.py
# Basic test to ensure FastAPI app import works
def test_app_import():
    from backend.app import app
    assert app is not None
