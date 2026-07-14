# config.py - Freedeck configuration and logging

import logging
import os
from pathlib import Path

try:
    import decky
except Exception:  # Local development and tests
    decky = None


def _decky_path(name: str, fallback: Path) -> str:
    value = getattr(decky, name, None) if decky is not None else None
    return str(Path(value).expanduser()) if value else str(fallback.expanduser())


def setup_logger() -> logging.Logger:
    """Initialize a Decky-compatible rotating-friendly logger target."""
    log_root = Path(_decky_path("DECKY_LOG_DIR", Path("/tmp")))
    try:
        log_root.mkdir(parents=True, exist_ok=True)
        log_file = log_root / "freedeck.log"
        logging.basicConfig(
            level=logging.INFO,
            filename=str(log_file),
            format="[%(asctime)s | %(filename)s:%(lineno)s:%(funcName)s] %(levelname)s: %(message)s",
            filemode="a",
            force=True,
        )
    except Exception:
        logging.basicConfig(
            level=logging.INFO,
            format="[%(asctime)s | %(filename)s:%(lineno)s:%(funcName)s] %(levelname)s: %(message)s",
            force=True,
        )
    return logging.getLogger("freedeck")


logger = setup_logger()
logger.setLevel(logging.INFO)

HOME_DIR = _decky_path("DECKY_USER_HOME", Path.home())
DOWNLOADS_DIR = str(Path(HOME_DIR) / "Downloads")
SHARE_DIR = str(Path(HOME_DIR) / ".local" / "share")

# New Decky Loader versions provide persistent settings/runtime/cache locations.
# Fall back to the legacy path so existing installations keep working.
DECKY_SETTINGS_DIR = _decky_path("DECKY_SETTINGS_DIR", Path(SHARE_DIR) / "Freedeck" / "settings")
DECKY_RUNTIME_DIR = _decky_path("DECKY_RUNTIME_DIR", Path(SHARE_DIR) / "Freedeck")
DECKY_CACHE_DIR = _decky_path("DECKY_CACHE_DIR", Path(HOME_DIR) / ".cache" / "Freedeck")
DECKY_SEND_DIR = DECKY_RUNTIME_DIR

# Bounded caches prevent long browsing sessions from exhausting Gaming Mode memory.
IMAGE_CACHE_MAX_ITEMS = 160
IMAGE_CACHE_MAX_BYTES = 192 * 1024 * 1024
IMAGE_CACHE_TTL_SECONDS = 7 * 24 * 3600
IMAGE_NEGATIVE_CACHE_TTL_SECONDS = 10 * 60

# Download recovery controls.
FAILED_DOWNLOAD_RETENTION_SECONDS = 24 * 3600
DOWNLOAD_CLEANUP_TIMEOUT_SECONDS = 12
DOWNLOAD_STALE_CONTROL_SUFFIXES = (".aria2", ".tmp", ".part", ".partial")

# Local service configuration. Loopback-only is intentional.
DEFAULT_SERVER_HOST = "127.0.0.1"
DEFAULT_SERVER_PORT = 59271
PORT_CHECK_RETRIES = 5
PORT_CHECK_RETRY_DELAY = 0.3
PORT_RELEASE_TIMEOUT = 5.0

SETTINGS_KEY = "freedeck_settings"
SETTING_RUNNING = "running"
SETTING_PORT = "port"
SETTING_DOWNLOAD_DIR = "download_dir"
