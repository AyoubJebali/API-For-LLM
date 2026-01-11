import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import os

# Set up test environment variables before importing main
os.environ["API_KEY"] = "test-api-key"

from main import app, API_KEYS_CREDITS


@pytest.fixture(autouse=True)
def reset_credits():
    """Reset API credits before each test."""
    API_KEYS_CREDITS["test-api-key"] = 10
    yield


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


class TestVerifyApiKey:
    """Tests for API key verification."""

    def test_missing_api_key(self, client):
        """Test that missing API key returns 403."""
        response = client.post("/generate", params={"promt": "Hello"})
        assert response.status_code == 403
        assert response.json()["detail"] == "Invalid or missing API Key"

    def test_invalid_api_key(self, client):
        """Test that invalid API key returns 403."""
        response = client.post(
            "/generate",
            params={"promt": "Hello"},
            headers={"x-api-key": "invalid-key"}
        )
        assert response.status_code == 403
        assert response.json()["detail"] == "Invalid or missing API Key"

    def test_zero_credits_api_key(self, client):
        """Test that API key with zero credits returns 403."""
        API_KEYS_CREDITS["test-api-key"] = 0
        response = client.post(
            "/generate",
            params={"promt": "Hello"},
            headers={"x-api-key": "test-api-key"}
        )
        assert response.status_code == 403


class TestGenerateEndpoint:
    """Tests for the /generate endpoint."""

    @patch("main.ollama")
    def test_generate_success(self, mock_ollama, client):
        """Test successful generation with valid API key."""
        mock_ollama.chat.return_value = {
            "message": {"content": "Hello! How can I help you?"}
        }

        response = client.post(
            "/generate",
            params={"promt": "Hello"},
            headers={"x-api-key": "test-api-key"}
        )

        assert response.status_code == 200
        assert response.json() == {"response": "Hello! How can I help you?"}
        mock_ollama.chat.assert_called_once_with(
            "llama2",
            messages=[{"role": "user", "content": "Hello"}]
        )

    @patch("main.ollama")
    def test_generate_decrements_credits(self, mock_ollama, client):
        """Test that each request decrements API credits."""
        mock_ollama.chat.return_value = {
            "message": {"content": "Response"}
        }
        initial_credits = API_KEYS_CREDITS["test-api-key"]

        client.post(
            "/generate",
            params={"promt": "Test"},
            headers={"x-api-key": "test-api-key"}
        )

        assert API_KEYS_CREDITS["test-api-key"] == initial_credits - 1

    @patch("main.ollama")
    def test_generate_with_long_prompt(self, mock_ollama, client):
        """Test generation with a longer prompt."""
        long_prompt = "This is a much longer prompt " * 10
        mock_ollama.chat.return_value = {
            "message": {"content": "Long response"}
        }

        response = client.post(
            "/generate",
            params={"promt": long_prompt},
            headers={"x-api-key": "test-api-key"}
        )

        assert response.status_code == 200
        mock_ollama.chat.assert_called_once_with(
            "llama2",
            messages=[{"role": "user", "content": long_prompt}]
        )

    @patch("main.ollama")
    def test_multiple_requests_exhaust_credits(self, mock_ollama, client):
        """Test that credits are exhausted after multiple requests."""
        API_KEYS_CREDITS["test-api-key"] = 2
        mock_ollama.chat.return_value = {
            "message": {"content": "Response"}
        }

        # First request - should succeed
        response1 = client.post(
            "/generate",
            params={"promt": "Test 1"},
            headers={"x-api-key": "test-api-key"}
        )
        assert response1.status_code == 200

        # Second request - should succeed
        response2 = client.post(
            "/generate",
            params={"promt": "Test 2"},
            headers={"x-api-key": "test-api-key"}
        )
        assert response2.status_code == 200

        # Third request - should fail (no credits left)
        response3 = client.post(
            "/generate",
            params={"promt": "Test 3"},
            headers={"x-api-key": "test-api-key"}
        )
        assert response3.status_code == 403
