"""Station and observation eligibility filters for land-plant ECWT composites."""

from __future__ import annotations


def _split_station_id(station_id: str | None) -> tuple[str, str] | None:
    text = (station_id or "").strip()
    if "-" not in text:
        return None
    usaf, wban = text.split("-", 1)
    if len(usaf) != 6 or len(wban) != 5:
        return None
    if not (usaf.isdigit() and wban.isdigit()):
        return None
    return usaf, wban


def is_marine_platform_station_id(station_id: str | None) -> bool:
    """Return true for NOAA ISD marine/buoy/C-MAN platform station IDs.

    ADR-0006 excludes these platform classes from land-plant composites:
    997xxx and 998xxx station prefixes, plus 999xxx records whose WBAN is the
    99999 marine placeholder.
    """
    parts = _split_station_id(station_id)
    if parts is None:
        return False
    usaf, wban = parts
    if usaf.startswith(("997", "998")):
        return True
    return usaf.startswith("999") and wban == "99999"


def is_marine_platform_report_type(report_type: str | None) -> bool:
    """Return true for NOAA FM-13 ship-format observations."""
    return (report_type or "").strip().upper() == "FM-13"


def is_land_plant_station_eligible(station_id: str | None) -> bool:
    return not is_marine_platform_station_id(station_id)


def is_land_plant_observation_eligible(
    station_id: str | None,
    report_type: str | None,
) -> bool:
    return (
        is_land_plant_station_eligible(station_id)
        and not is_marine_platform_report_type(report_type)
    )
