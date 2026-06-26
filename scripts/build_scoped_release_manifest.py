#!/usr/bin/env python3
"""Build an auditable manifest for a scoped plant ECWT release."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import subprocess
from collections import OrderedDict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from eop012_config import PROJECT_ROOT, PSQL

METHODOLOGY_VERSION_FALLBACK = "eop012-ecwt-method-v0.2.0"
RELEASE_PREFIX = "scoped_plant_ecwt_release_"
MANIFEST_RUN_PREFIX = "release_manifest_"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def sql_literal(value: object) -> str:
    if value is None:
        return "null"
    return "'" + str(value).replace("'", "''") + "'"


def run(cmd: list[str], *, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        cmd,
        input=input_text,
        text=True,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        raise RuntimeError(
            "Command failed with exit code "
            f"{result.returncode}: {' '.join(cmd)}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
        )
    return result


def psql_cmd(psql: Path, host: str, port: int, dbname: str, user: str | None) -> list[str]:
    cmd = [str(psql), "-h", host, "-p", str(port)]
    if user:
        cmd.extend(["-U", user])
    cmd.extend(["-d", dbname, "-v", "ON_ERROR_STOP=1"])
    return cmd


def psql_scalar(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    query: str,
) -> str:
    result = run(psql_cmd(psql, host, port, dbname, user) + ["-At", "-c", query])
    return result.stdout.strip()


def psql_csv_query(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    query: str,
) -> list[dict[str, str]]:
    result = run(
        psql_cmd(psql, host, port, dbname, user)
        + ["-c", f"\\copy ({query}) to stdout with (format csv, header true)"]
    )
    return list(csv.DictReader(io.StringIO(result.stdout)))


def psql_execute(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    sql: str,
) -> None:
    run(psql_cmd(psql, host, port, dbname, user) + ["-c", sql])


def git_commit_label(project_root: Path) -> str:
    commit = run(["git", "-C", str(project_root), "rev-parse", "HEAD"]).stdout.strip()
    dirty = run(["git", "-C", str(project_root), "status", "--porcelain"]).stdout.strip()
    return f"{commit}-dirty" if dirty else commit


def latest_scoped_release_id(project_root: Path) -> str:
    processed_dir = project_root / "data" / "processed"
    candidates = [
        path
        for path in processed_dir.glob(f"{RELEASE_PREFIX}*.csv")
        if not path.name.endswith("_exclusions.csv")
    ]
    if not candidates:
        raise RuntimeError(f"No scoped release CSV found under {processed_dir}.")
    latest = max(candidates, key=lambda path: path.stat().st_mtime)
    return latest.stem


def latest_status_doc(project_root: Path) -> Path | None:
    docs_dir = project_root / "docs"
    candidates = sorted(docs_dir.glob("noaa_backfill_load_policy_refresh_*.md"))
    return candidates[-1] if candidates else None


def parse_backticked_fields(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    values: dict[str, str] = {}
    field_pattern = re.compile(r"^- (?P<label>[^:]+): `(?P<value>[^`]+)`")
    range_pattern = re.compile(r"^- NOAA DJF load runs: `(?P<start>[^`]+)` through `(?P<end>[^`]+)`")
    for line in path.read_text(encoding="utf-8").splitlines():
        range_match = range_pattern.match(line)
        if range_match:
            values["NOAA DJF load run start"] = range_match.group("start")
            values["NOAA DJF load run end"] = range_match.group("end")
            continue
        field_match = field_pattern.match(line)
        if field_match:
            values[field_match.group("label")] = field_match.group("value")
    return values


def first_present(*values: str | None) -> str | None:
    for value in values:
        if value:
            return value
    return None


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def csv_row_count(path: Path) -> int:
    with path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        try:
            next(reader)
        except StopIteration:
            return 0
        return sum(1 for _ in reader)


def artifact_type(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return "csv"
    if suffix == ".md":
        return "markdown"
    if suffix == ".json":
        return "json"
    if suffix == ".py":
        return "python"
    if suffix == ".sql":
        return "sql"
    return suffix.lstrip(".") or "file"


def relative_path(project_root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(project_root))
    except ValueError:
        return str(path)


def artifact_record(project_root: Path, name: str, path: Path) -> OrderedDict[str, object]:
    path = path.resolve()
    record: OrderedDict[str, object] = OrderedDict(
        [
            ("artifact_name", name),
            ("artifact_type", artifact_type(path)),
            ("path", relative_path(project_root, path)),
            ("exists", path.exists()),
        ]
    )
    if path.exists():
        record["size_bytes"] = path.stat().st_size
        record["sha256"] = sha256_file(path)
        record["row_count"] = csv_row_count(path) if path.suffix.lower() == ".csv" else None
    else:
        record["size_bytes"] = None
        record["sha256"] = None
        record["row_count"] = None
    return record


def existing_artifacts(
    project_root: Path,
    release_id: str,
    run_ids: dict[str, str | None],
    status_doc: Path | None,
) -> list[OrderedDict[str, object]]:
    docs_dir = project_root / "docs"
    processed_dir = project_root / "data" / "processed"
    paths: list[tuple[str, Path]] = [
        ("release_dataset_csv", processed_dir / f"{release_id}.csv"),
        ("release_exclusions_csv", processed_dir / f"{release_id}_exclusions.csv"),
        ("release_report_md", docs_dir / f"{release_id}_report.md"),
    ]
    if status_doc:
        paths.append(("noaa_backfill_load_policy_refresh_md", status_doc))
    optional_paths = [
        ("methodology_md", docs_dir / "methodology.md"),
        ("readme_md", project_root / "README.md"),
        ("audit_schema_sql", project_root / "sql" / "audit_schema.sql"),
        ("data_dictionary_md", docs_dir / "data_dictionary.md"),
        ("scoped_export_script_py", project_root / "scripts" / "export_scoped_plant_ecwt_dataset.py"),
        ("manifest_builder_script_py", project_root / "scripts" / "build_scoped_release_manifest.py"),
    ]
    run_artifact_patterns = [
        ("policy_result_csv", run_ids.get("policy_result_run_id"), ".csv"),
        ("policy_result_report_md", run_ids.get("policy_result_run_id"), "_report.md"),
        ("secondary_fill_plants_csv", run_ids.get("secondary_fill_run_id"), "_plants.csv"),
        ("secondary_fill_candidate_scores_csv", run_ids.get("secondary_fill_run_id"), "_candidate_scores.csv"),
        ("secondary_fill_report_md", run_ids.get("secondary_fill_run_id"), "_report.md"),
        ("station_ecwt_report_md", run_ids.get("station_ecwt_run_id"), "_report.md"),
        ("station_year_coverage_report_md", run_ids.get("coverage_run_id"), "_report.md"),
        ("plant_ecwt_report_md", run_ids.get("plant_ecwt_run_id"), "_report.md"),
        ("plant_readiness_report_md", run_ids.get("readiness_run_id"), "_report.md"),
        ("denominator_diagnostic_csv", run_ids.get("denominator_diagnostic_run_id"), ".csv"),
        ("denominator_diagnostic_report_md", run_ids.get("denominator_diagnostic_run_id"), "_report.md"),
        ("policy_scenarios_db_load_report_md", run_ids.get("scenario_db_load_run_id"), "_report.md"),
    ]
    for name, run_id, suffix in run_artifact_patterns:
        if run_id:
            paths.append((name, docs_dir / f"{run_id}{suffix}"))
    paths.extend(optional_paths)

    seen: set[Path] = set()
    records: list[OrderedDict[str, object]] = []
    for name, path in paths:
        resolved = path.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        record = artifact_record(project_root, name, resolved)
        if record["exists"]:
            records.append(record)
    return records


def run_row(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    run_id: str | None,
) -> dict[str, str] | None:
    if not run_id:
        return None
    rows = psql_csv_query(
        psql,
        host,
        port,
        dbname,
        user,
        f"""
        select calculation_run_id, methodology_version, run_status, code_commit,
               run_started_at_utc, run_finished_at_utc, notes
        from audit.calculation_run
        where calculation_run_id = {sql_literal(run_id)}
        """,
    )
    return rows[0] if rows else None


def db_evidence(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    run_ids: dict[str, str | None],
) -> OrderedDict[str, object]:
    evidence: OrderedDict[str, object] = OrderedDict()
    inventory_run_id = run_ids.get("raw_inventory_run_id")
    manifest_run_id = run_ids.get("backfill_manifest_run_id")
    coverage_run_id = run_ids.get("coverage_run_id")
    station_ecwt_run_id = run_ids.get("station_ecwt_run_id")
    policy_result_run_id = run_ids.get("policy_result_run_id")
    secondary_fill_run_id = run_ids.get("secondary_fill_run_id")
    load_start = run_ids.get("load_run_start")
    load_end = run_ids.get("load_run_end")

    if inventory_run_id:
        evidence["raw_inventory"] = psql_csv_query(
            psql,
            host,
            port,
            dbname,
            user,
            f"""
            select file_status, count(*)::bigint as station_years
            from weather.noaa_raw_file_inventory
            where calculation_run_id = {sql_literal(inventory_run_id)}
            group by file_status
            order by file_status
            """,
        )
    if manifest_run_id:
        evidence["backfill_manifest"] = psql_csv_query(
            psql,
            host,
            port,
            dbname,
            user,
            f"""
            select manifest_status, count(*)::bigint as station_years
            from weather.noaa_raw_backfill_manifest
            where calculation_run_id = {sql_literal(manifest_run_id)}
            group by manifest_status
            order by manifest_status
            """,
        )
    if load_start and load_end:
        evidence["noaa_djf_loads"] = psql_csv_query(
            psql,
            host,
            port,
            dbname,
            user,
            f"""
            with bounds as (
                select min(run_started_at_utc) as min_started_at_utc,
                       max(run_started_at_utc) as max_started_at_utc
                from audit.calculation_run
                where calculation_run_id in ({sql_literal(load_start)}, {sql_literal(load_end)})
            ),
            load_runs as (
                select calculation_run_id
                from audit.calculation_run r
                cross join bounds b
                where r.calculation_run_id like 'noaa_hourly_djf_load_%'
                  and r.run_started_at_utc between b.min_started_at_utc and b.max_started_at_utc
            )
            select file_status,
                   count(*)::bigint as files,
                   coalesce(sum(loaded_hour_count), 0)::bigint as loaded_hours,
                   coalesce(sum(invalid_temp_rows), 0)::bigint as invalid_temp_rows,
                   coalesce(sum(rejected_source_rows), 0)::bigint as rejected_source_rows,
                   coalesce(sum(duplicate_hour_count), 0)::bigint as duplicate_hours
            from weather.noaa_hourly_load_file
            where calculation_run_id in (select calculation_run_id from load_runs)
            group by file_status
            order by file_status
            """,
        )
    if coverage_run_id:
        evidence["station_year_coverage"] = psql_csv_query(
            psql,
            host,
            port,
            dbname,
            user,
            f"""
            with coverage_rows as (
                select coverage_status
                from weather.station_year_djf_coverage
                where calculation_run_id = {sql_literal(coverage_run_id)}
                union all
                select coverage_status
                from weather.station_year_djf_coverage_current
                where calculation_run_id = {sql_literal(coverage_run_id)}
            )
            select coverage_status, count(*)::bigint as station_years
            from coverage_rows
            group by coverage_status
            order by coverage_status
            """,
        )
    if station_ecwt_run_id:
        evidence["station_ecwt"] = psql_csv_query(
            psql,
            host,
            port,
            dbname,
            user,
            f"""
            select result_status, count(*)::bigint as stations
            from calc.station_ecwt
            where calculation_run_id = {sql_literal(station_ecwt_run_id)}
            group by result_status
            order by result_status
            """,
        )
    if policy_result_run_id:
        evidence["policy_result"] = psql_csv_query(
            psql,
            host,
            port,
            dbname,
            user,
            f"""
            select readiness_status, reason_code, count(*)::bigint as plants
            from calc.plant_ecwt_policy_result
            where policy_result_run_id = {sql_literal(policy_result_run_id)}
            group by readiness_status, reason_code
            order by readiness_status, reason_code
            """,
        )
    if secondary_fill_run_id:
        evidence["secondary_fill"] = psql_csv_query(
            psql,
            host,
            port,
            dbname,
            user,
            f"""
            select fill_status, count(*)::bigint as plants
            from calc.plant_ecwt_secondary_fill
            where secondary_fill_run_id = {sql_literal(secondary_fill_run_id)}
            group by fill_status
            order by fill_status
            """,
        )
    return evidence


def render_markdown(
    path: Path,
    manifest: OrderedDict[str, object],
    manifest_json_sha256: str,
    manifest_json_path: Path,
    displayed_artifacts: Iterable[OrderedDict[str, object]],
) -> None:
    artifacts = list(displayed_artifacts)
    run_chain = manifest["run_chain"]
    evidence = manifest["db_evidence"]
    lines = [
        "# Scoped Plant ECWT Release Manifest",
        "",
        f"- Release ID: `{manifest['release_id']}`",
        f"- Release name: `{manifest['release_name']}`",
        f"- Manifest run ID: `{manifest['manifest_run_id']}`",
        f"- Generated UTC: {manifest['generated_at_utc']}",
        f"- Git generation commit: `{manifest['git_generation_commit']}`",
        f"- Manifest JSON: `{relative_path(Path(manifest['project_root']), manifest_json_path)}`",
        f"- Manifest JSON SHA-256: `{manifest_json_sha256}`",
        "",
        "## Scope",
        "",
        "This release publishes non-Alaska plant-level ECWT rows that passed the normalized active-window loaded-year policy or the documented secondary-station fill policy. Alaska rows and reviewed no-station edge cases are excluded from the current scoped denominator and published in the exclusions CSV.",
        "",
        "## Run Chain",
        "",
        "| Role | Calculation Run ID | Status | Code Commit |",
        "| --- | --- | --- | --- |",
    ]
    for item in run_chain:
        lines.append(
            f"| {item['role']} | `{item['calculation_run_id']}` | "
            f"{item.get('run_status') or ''} | `{item.get('code_commit') or ''}` |"
        )
    lines.extend(
        [
            "",
            "## Artifact Checksums",
            "",
            "| Artifact | Type | Rows | Size Bytes | SHA-256 | Path |",
            "| --- | --- | ---: | ---: | --- | --- |",
        ]
    )
    for artifact in artifacts:
        rows = "" if artifact["row_count"] is None else artifact["row_count"]
        size = "" if artifact["size_bytes"] is None else artifact["size_bytes"]
        lines.append(
            f"| {artifact['artifact_name']} | {artifact['artifact_type']} | {rows} | {size} | "
            f"`{artifact['sha256']}` | `{artifact['path']}` |"
        )
    lines.extend(["", "## Database Evidence", ""])
    for section, rows in evidence.items():
        lines.append(f"### {section.replace('_', ' ').title()}")
        lines.append("")
        if not rows:
            lines.append("_No rows returned._")
            lines.append("")
            continue
        headers = list(rows[0].keys())
        lines.append("| " + " | ".join(headers) + " |")
        lines.append("| " + " | ".join("---" for _ in headers) + " |")
        for row in rows:
            lines.append("| " + " | ".join(row.get(header, "") for header in headers) + " |")
        lines.append("")
    lines.extend(
        [
            "## Notes",
            "",
            "- This manifest records the current public analytical release, not a final Generator Owner compliance filing.",
            "- Heavy NOAA raw data and the Postgres working cluster are external build inputs and are not committed to Git.",
            "- The Git tag for the release should point to the commit containing this manifest and the release artifacts.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def upsert_release_manifest(
    psql: Path,
    host: str,
    port: int,
    dbname: str,
    user: str | None,
    manifest: OrderedDict[str, object],
    manifest_json_sha256: str,
    db_artifacts: Iterable[OrderedDict[str, object]],
) -> None:
    release_id = str(manifest["release_id"])
    manifest_run_id = str(manifest["manifest_run_id"])
    methodology_version = str(manifest["methodology_version"])
    git_commit = str(manifest["git_generation_commit"])
    generated_at = str(manifest["generated_at_utc"])
    db_artifacts = list(db_artifacts)
    parameters_json = json.dumps(
        {
            "release_id": release_id,
            "source_run_ids": manifest["source_run_ids"],
            "artifact_count": len(db_artifacts),
        },
        sort_keys=True,
    )
    release_notes = (
        "Scoped non-Alaska plant ECWT release with reviewed no-station edge cases excluded "
        "and documented secondary-station fill rows included."
    )
    statements = [
        f"""
        insert into audit.calculation_run (
            calculation_run_id, methodology_version, code_commit, run_started_at_utc,
            run_finished_at_utc, run_status, parameters_json, notes
        )
        values (
            {sql_literal(manifest_run_id)},
            {sql_literal(methodology_version)},
            {sql_literal(git_commit)},
            {sql_literal(generated_at)}::timestamptz,
            now(),
            'succeeded',
            {sql_literal(parameters_json)}::jsonb,
            'Generated scoped release manifest.'
        )
        on conflict (calculation_run_id) do update set
            code_commit = excluded.code_commit,
            run_finished_at_utc = excluded.run_finished_at_utc,
            run_status = excluded.run_status,
            parameters_json = excluded.parameters_json,
            notes = excluded.notes;
        """,
        f"""
        insert into audit.release_manifest (
            release_id, calculation_run_id, release_name, release_created_at_utc,
            code_commit, source_manifest_sha256, release_notes
        )
        values (
            {sql_literal(release_id)},
            {sql_literal(manifest_run_id)},
            {sql_literal(manifest["release_name"])},
            {sql_literal(generated_at)}::timestamptz,
            {sql_literal(git_commit)},
            {sql_literal(manifest_json_sha256)},
            {sql_literal(release_notes)}
        )
        on conflict (release_id) do update set
            calculation_run_id = excluded.calculation_run_id,
            release_name = excluded.release_name,
            release_created_at_utc = excluded.release_created_at_utc,
            code_commit = excluded.code_commit,
            source_manifest_sha256 = excluded.source_manifest_sha256,
            release_notes = excluded.release_notes;
        """,
    ]
    for artifact in db_artifacts:
        artifact_id = f"{release_id}:{artifact['artifact_name']}"
        statements.append(
            f"""
            insert into publish.release_artifact (
                release_artifact_id, release_id, artifact_name, artifact_type,
                local_path, size_bytes, sha256, row_count
            )
            values (
                {sql_literal(artifact_id)},
                {sql_literal(release_id)},
                {sql_literal(artifact["artifact_name"])},
                {sql_literal(artifact["artifact_type"])},
                {sql_literal(artifact["path"])},
                {sql_literal(artifact["size_bytes"])},
                {sql_literal(artifact["sha256"])},
                {sql_literal(artifact["row_count"])}
            )
            on conflict (release_artifact_id) do update set
                artifact_type = excluded.artifact_type,
                local_path = excluded.local_path,
                size_bytes = excluded.size_bytes,
                sha256 = excluded.sha256,
                row_count = excluded.row_count,
                created_at_utc = now();
            """
        )
    psql_execute(psql, host, port, dbname, user, "begin;\n" + "\n".join(statements) + "\ncommit;")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project-root", type=Path, default=PROJECT_ROOT)
    parser.add_argument("--psql", type=Path, default=PSQL)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5436)
    parser.add_argument("--dbname", default="eop012")
    parser.add_argument("--user", default=None)
    parser.add_argument("--release-id")
    parser.add_argument("--status-doc", type=Path)
    parser.add_argument("--raw-inventory-run-id")
    parser.add_argument("--backfill-manifest-run-id")
    parser.add_argument("--load-run-start")
    parser.add_argument("--load-run-end")
    parser.add_argument("--coverage-run-id")
    parser.add_argument("--station-ecwt-run-id")
    parser.add_argument("--plant-ecwt-run-id")
    parser.add_argument("--readiness-run-id")
    parser.add_argument("--denominator-diagnostic-run-id")
    parser.add_argument("--scenario-db-load-run-id")
    parser.add_argument("--policy-result-run-id")
    parser.add_argument("--secondary-fill-run-id")
    parser.add_argument("--skip-db", action="store_true")
    args = parser.parse_args()

    project_root = args.project_root.resolve()
    release_id = args.release_id or latest_scoped_release_id(project_root)
    release_report = project_root / "docs" / f"{release_id}_report.md"
    status_doc = args.status_doc or latest_status_doc(project_root)
    release_fields = parse_backticked_fields(release_report)
    status_fields = parse_backticked_fields(status_doc) if status_doc else {}

    run_ids: dict[str, str | None] = {
        "raw_inventory_run_id": first_present(args.raw_inventory_run_id, status_fields.get("Raw-file inventory run ID")),
        "backfill_manifest_run_id": first_present(
            args.backfill_manifest_run_id, status_fields.get("Backfill manifest run ID")
        ),
        "load_run_start": first_present(args.load_run_start, status_fields.get("NOAA DJF load run start")),
        "load_run_end": first_present(args.load_run_end, status_fields.get("NOAA DJF load run end")),
        "coverage_run_id": first_present(args.coverage_run_id, status_fields.get("Station-year coverage run ID")),
        "station_ecwt_run_id": first_present(
            args.station_ecwt_run_id,
            release_fields.get("Station ECWT run ID"),
            status_fields.get("Station ECWT run ID"),
        ),
        "plant_ecwt_run_id": first_present(args.plant_ecwt_run_id, status_fields.get("Fixed-period plant ECWT run ID")),
        "readiness_run_id": first_present(args.readiness_run_id, status_fields.get("Fixed-period readiness run ID")),
        "denominator_diagnostic_run_id": first_present(
            args.denominator_diagnostic_run_id,
            status_fields.get("Denominator diagnostic run ID"),
        ),
        "scenario_db_load_run_id": first_present(
            args.scenario_db_load_run_id,
            status_fields.get("Policy scenario DB load run ID"),
        ),
        "policy_result_run_id": first_present(
            args.policy_result_run_id,
            release_fields.get("Policy result run ID"),
            status_fields.get("Policy result run ID"),
        ),
        "secondary_fill_run_id": first_present(
            args.secondary_fill_run_id,
            release_fields.get("Secondary fill run ID"),
            status_fields.get("Secondary station fill run ID"),
        ),
    }

    required = ["policy_result_run_id", "secondary_fill_run_id", "station_ecwt_run_id"]
    missing_required = [name for name in required if not run_ids.get(name)]
    if missing_required:
        raise RuntimeError(f"Missing required run IDs: {', '.join(missing_required)}")

    policy_row = run_row(
        args.psql,
        args.host,
        args.port,
        args.dbname,
        args.user,
        run_ids["policy_result_run_id"],
    )
    methodology_version = (
        policy_row["methodology_version"] if policy_row else METHODOLOGY_VERSION_FALLBACK
    )
    generated_at = utc_now().isoformat(timespec="seconds").replace("+00:00", "Z")
    manifest_run_id = f"{MANIFEST_RUN_PREFIX}{generated_at.replace('-', '').replace(':', '').replace('Z', 'Z')}"
    manifest_run_id = manifest_run_id.replace("T", "T")
    git_commit = git_commit_label(project_root)

    roles = [
        ("raw inventory", run_ids.get("raw_inventory_run_id")),
        ("backfill manifest", run_ids.get("backfill_manifest_run_id")),
        ("NOAA DJF load start", run_ids.get("load_run_start")),
        ("NOAA DJF load end", run_ids.get("load_run_end")),
        ("station-year DJF coverage", run_ids.get("coverage_run_id")),
        ("station ECWT", run_ids.get("station_ecwt_run_id")),
        ("fixed-period plant ECWT", run_ids.get("plant_ecwt_run_id")),
        ("fixed-period readiness", run_ids.get("readiness_run_id")),
        ("denominator diagnostic", run_ids.get("denominator_diagnostic_run_id")),
        ("policy scenario DB load", run_ids.get("scenario_db_load_run_id")),
        ("policy result", run_ids.get("policy_result_run_id")),
        ("secondary station fill", run_ids.get("secondary_fill_run_id")),
    ]
    run_chain = []
    for role, run_id in roles:
        row = run_row(args.psql, args.host, args.port, args.dbname, args.user, run_id)
        if row:
            item = OrderedDict([("role", role)])
            item.update(row)
            run_chain.append(item)
        elif run_id:
            run_chain.append(OrderedDict([("role", role), ("calculation_run_id", run_id)]))

    artifacts = existing_artifacts(project_root, release_id, run_ids, status_doc)
    evidence = db_evidence(args.psql, args.host, args.port, args.dbname, args.user, run_ids)

    manifest = OrderedDict(
        [
            ("release_id", release_id),
            ("release_name", f"Scoped plant ECWT release {release_id.removeprefix(RELEASE_PREFIX)}"),
            ("manifest_run_id", manifest_run_id),
            ("generated_at_utc", generated_at),
            ("project_root", str(project_root)),
            ("methodology_version", methodology_version),
            ("git_generation_commit", git_commit),
            ("scope", "non-Alaska plant-level publication-ready ECWT rows; reviewed no-station edge cases excluded"),
            ("source_run_ids", run_ids),
            ("run_chain", run_chain),
            ("artifacts", artifacts),
            ("db_evidence", evidence),
        ]
    )

    docs_dir = project_root / "docs"
    manifest_json_path = docs_dir / f"{release_id}_manifest.json"
    manifest_md_path = docs_dir / f"{release_id}_manifest.md"
    manifest_json_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    manifest_json_sha256 = sha256_file(manifest_json_path)

    # The JSON manifest deliberately does not include its own checksum, and the
    # Markdown report deliberately does not include its own checksum. The DB
    # artifact rows record both manifest-file checksums after rendering.
    manifest_json_artifact = artifact_record(project_root, "release_manifest_json", manifest_json_path)
    displayed_artifacts = list(manifest["artifacts"]) + [manifest_json_artifact]
    render_markdown(manifest_md_path, manifest, manifest_json_sha256, manifest_json_path, displayed_artifacts)
    manifest_md_artifact = artifact_record(project_root, "release_manifest_md", manifest_md_path)
    db_artifacts = list(manifest["artifacts"]) + [manifest_json_artifact, manifest_md_artifact]

    if not args.skip_db:
        upsert_release_manifest(
            args.psql,
            args.host,
            args.port,
            args.dbname,
            args.user,
            manifest,
            manifest_json_sha256,
            db_artifacts,
        )

    print(
        json.dumps(
            OrderedDict(
                [
                    ("release_id", release_id),
                    ("manifest_run_id", manifest_run_id),
                    ("manifest_json", str(manifest_json_path)),
                    ("manifest_markdown", str(manifest_md_path)),
                    ("manifest_json_sha256", manifest_json_sha256),
                    ("artifact_count", len(db_artifacts)),
                    ("db_updated", not args.skip_db),
                ]
            ),
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
