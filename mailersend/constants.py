import platform
import sys

# Base API information
API_VERSION = "v1"
DEFAULT_BASE_URL = f"https://api.mailersend.com/{API_VERSION}"
DEFAULT_TIMEOUT = 30  # seconds

# Package info for user agent
PACKAGE_NAME = "mailersend-python"
__version__ = "2.0.0"

USER_AGENT = (
    f"{PACKAGE_NAME}/{__version__} "
    f"(Python/{platform.python_version()}; "
    f"OS/{platform.system()} {platform.release()}; "
    f"Impl/{platform.python_implementation()})"
)