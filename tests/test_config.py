import pytest

from app.core import config


def test_production_requires_a_real_secret_key(monkeypatch):
    monkeypatch.setattr(config, "ENVIRONMENT", "production")
    monkeypatch.setattr(config, "SECRET_KEY", config.DEFAULT_SECRET_KEY)
    with pytest.raises(RuntimeError):
        config.check_settings()


def test_production_accepts_a_custom_secret_key(monkeypatch):
    monkeypatch.setattr(config, "ENVIRONMENT", "production")
    monkeypatch.setattr(config, "SECRET_KEY", "a-long-random-value-for-this-test")
    config.check_settings()


def test_development_allows_the_default_secret_key(monkeypatch):
    monkeypatch.setattr(config, "ENVIRONMENT", "development")
    monkeypatch.setattr(config, "SECRET_KEY", config.DEFAULT_SECRET_KEY)
    config.check_settings()