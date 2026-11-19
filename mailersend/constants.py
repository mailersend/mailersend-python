import platform
import re
from importlib.metadata import PackageNotFoundError, version

# Base API information
API_HOST = "https://api.mailersend.com"
DEFAULT_API_VERSION = "2026-10"
API_VERSION_PATTERN = re.compile(r"^(v1|\d{4}-(0[1-9]|1[0-2]))$")
DEFAULT_BASE_URL = f"{API_HOST}/{DEFAULT_API_VERSION}/"
DEFAULT_TIMEOUT = 30  # seconds

# Package info for user agent
PACKAGE_NAME = "mailersend-python"
# The version comes from the git tag at build time; see [tool.hatch.version].
try:
    __version__ = version("mailersend")
except PackageNotFoundError:
    __version__ = "0.0.0.dev0"

USER_AGENT = (
    f"{PACKAGE_NAME}/{__version__} "
    f"(Python/{platform.python_version()}; "
    f"OS/{platform.system()} {platform.release()}; "
    f"Impl/{platform.python_implementation()})"
)
