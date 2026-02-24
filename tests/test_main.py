from fastapi.testclient import TestClient
from main import app
import os
import logging
import pytest

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_log_file():
    """Ensure the log file is clean before and after each test."""
    log_file = "yes.log.csv"
    if os.path.exists(log_file):
        os.remove(log_file)

    # We must recreate the handler to force it to open a new file
    # Otherwise logging keeps its handle on the deleted file
    import main

    for h in main.logger.handlers:
        h.close()
        main.logger.removeHandler(h)

    new_handler = logging.FileHandler("yes.log.csv", "a", "utf-8")
    new_handler.setFormatter(main.formatter)
    main.logger.addHandler(new_handler)

    yield

    for h in main.logger.handlers:
        h.close()

    if os.path.exists(log_file):
        os.remove(log_file)


def test_root_path_returns_ok():
    """Test that a basic GET request returns OK and logs the request."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.text == "OK"

    # Read the log file to verify logging middleware worked
    with open("yes.log.csv", "r") as f:
        logs = f.readlines()
        assert len(logs) == 1
        assert "GET;/" in logs[0]


def test_favicon_request():
    """Test that a request for favicon.ico is handled correctly."""
    response = client.get("/favicon.ico")
    assert response.status_code == 200
    assert response.text == "favicon"

    # Verify favicon requests are NOT logged by checking the file
    # We must close existing handlers to flush anything, though the testclient is synchronous
    with open("yes.log.csv", "r") as f:
        logs = f.readlines()
        assert len(logs) == 0


def test_different_http_methods():
    """Test that other HTTP methods are logged."""
    response = client.post("/submit")
    assert response.status_code == 200
    assert response.text == "OK"

    with open("yes.log.csv", "r") as f:
        logs = f.readlines()
        assert len(logs) == 1
        assert "POST;/submit" in logs[0]
