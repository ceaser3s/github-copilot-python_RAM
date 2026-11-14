"""Shared pytest fixtures for the Flask application."""

from collections.abc import Iterator

import pytest
from flask.testing import FlaskClient

import app as app_module


@pytest.fixture
def client() -> Iterator[FlaskClient]:
    """Provide an isolated Flask test client."""
    app_module.app.config.update(TESTING=True)
    app_module.CURRENT.update(
        puzzle=None, solution=None, hints_used=0, hint_cells=[]
    )
    with app_module.app.test_client() as test_client:
        yield test_client
    app_module.CURRENT.update(
        puzzle=None, solution=None, hints_used=0, hint_cells=[]
    )
