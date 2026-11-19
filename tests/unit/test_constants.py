"""Tests for the SDK version reported in the User-Agent."""

import importlib
from importlib.metadata import PackageNotFoundError
from unittest.mock import patch

import mailersend
from mailersend import constants


class TestVersion:
    def teardown_method(self):
        importlib.reload(constants)

    def test_version_comes_from_installed_package_metadata(self):
        with patch("importlib.metadata.version", return_value="9.8.7"):
            importlib.reload(constants)

        assert constants.__version__ == "9.8.7"
        assert constants.USER_AGENT.startswith("mailersend-python/9.8.7 ")

    def test_version_falls_back_when_package_is_not_installed(self):
        with patch(
            "importlib.metadata.version", side_effect=PackageNotFoundError("mailersend")
        ):
            importlib.reload(constants)

        assert constants.__version__ == "0.0.0.dev0"
        assert constants.USER_AGENT.startswith("mailersend-python/0.0.0.dev0 ")

    def test_package_exports_the_version(self):
        assert mailersend.__version__ == constants.__version__
