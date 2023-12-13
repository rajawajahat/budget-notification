"""Module that is automatically imported into tests, contains fixtures."""
import logging
from unittest.mock import patch

from pytest import fixture


@fixture(scope="class")
def mock_logger():
    with patch.object(logging, "exception") as logger:
        yield logger
