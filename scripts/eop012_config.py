"""Shared environment-backed defaults for EOP012 command-line scripts."""

from __future__ import annotations

import os
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def env_path(name: str, default: Path | str) -> Path:
    value = os.environ.get(name)
    if value:
        return Path(value).expanduser()
    return Path(default).expanduser()


def env_path_list(name: str, default: list[Path]) -> list[Path]:
    value = os.environ.get(name)
    if not value:
        return default
    return [Path(part).expanduser() for part in value.split(os.pathsep) if part]


PROJECT_ROOT = env_path("EOP012_PROJECT_ROOT", REPO_ROOT)
DATA_ROOT = env_path("EOP012_DATA_ROOT", Path.home() / "eop012_data")
STAGING_ROOT = env_path("EOP012_STAGING_ROOT", DATA_ROOT / "staging")
EIA860_ZIP = env_path("EOP012_EIA860_ZIP", DATA_ROOT / "raw" / "eia860" / "intake" / "eia8602024.zip")
NOAA_GLOBAL_HOURLY_ROOT = env_path(
    "EOP012_NOAA_GLOBAL_HOURLY_ROOT",
    DATA_ROOT / "raw" / "noaa" / "global-hourly",
)
STATION_HISTORY_CSV = env_path(
    "EOP012_STATION_HISTORY_CSV",
    DATA_ROOT / "raw" / "noaa" / "isd-history.csv",
)
SOURCE_CLUSTER_PATH = env_path(
    "EOP012_SOURCE_CLUSTER_PATH",
    DATA_ROOT / "legacy" / "postgres16_weather_build_5435",
)
PSQL = env_path("EOP012_PSQL", "psql")
NOAA_RAW_ROOTS = env_path_list("EOP012_NOAA_RAW_ROOTS", [NOAA_GLOBAL_HOURLY_ROOT])
