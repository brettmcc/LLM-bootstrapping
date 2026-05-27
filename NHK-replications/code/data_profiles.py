"""Helpers for the expanded ACS extract used by the current pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


EXPANDED_DATA_PROFILE = "expanded"
DEFAULT_DATA_PROFILE = EXPANDED_DATA_PROFILE


@dataclass(frozen=True)
class DataProfile:
    # This dataclass keeps the filenames and output naming rules together.
    name: str
    description: str
    data_file_name: str
    layout_file_name: str
    run_data_file_name: str
    run_layout_excerpt_name: str
    aggregate_csv_name: str


DATA_PROFILES: dict[str, DataProfile] = {
    EXPANDED_DATA_PROFILE: DataProfile(
        name=EXPANDED_DATA_PROFILE,
        description="Expanded ACS extract covering the superset of submitted-replication variables.",
        data_file_name="ACS_extract_expanded.dat",
        layout_file_name="acs_extra_expanded.do",
        run_data_file_name="ACS_extract_expanded.dat",
        run_layout_excerpt_name="ACS_extract_expanded_layout_excerpt.do",
        aggregate_csv_name="runs_complete_expanded.csv",
    ),
}


def get_data_profile(name: str) -> DataProfile:
    # Raise a clear error if a caller asks for an unknown profile name.
    try:
        return DATA_PROFILES[name]
    except KeyError as exc:
        allowed = ", ".join(sorted(DATA_PROFILES))
        raise ValueError(f"Unknown data profile: {name}. Expected one of: {allowed}") from exc


def replication_materials_dir(project: Path) -> Path:
    # The ACS extract files and supporting policy inputs live in replication-materials.
    return project / "replication-materials"


def data_file_path(project: Path, profile_name: str) -> Path:
    # Return the ACS data file path for the selected profile.
    profile = get_data_profile(profile_name)
    return replication_materials_dir(project) / profile.data_file_name


def layout_file_path(project: Path, profile_name: str) -> Path:
    # Return the IPUMS layout .do file path for the selected profile.
    profile = get_data_profile(profile_name)
    return replication_materials_dir(project) / profile.layout_file_name


def specs_base_dir(project: Path, profile_name: str, *, phase12: bool = False) -> Path:
    # Current Phase 12 specs live directly under specs/spec_<run_id>.json.
    if phase12:
        get_data_profile(profile_name)
        return project / "specs"

    base = project / "specs"
    profile = get_data_profile(profile_name)
    return base / profile.name


def specs_dir(project: Path, provider: str, profile_name: str, *, phase12: bool = False) -> Path:
    # Provider-specific spec directory for the selected data profile.
    if phase12:
        return specs_base_dir(project, profile_name, phase12=True)
    return specs_base_dir(project, profile_name, phase12=phase12) / provider


def executions_root(project: Path, profile_name: str, *, phase12: bool = False) -> Path:
    # Current Phase 12 run directories live directly under runs/<run_id>.
    if phase12:
        get_data_profile(profile_name)
        return project / "runs"

    # Keep the historical non-Phase-12 layout for any older helper callers.
    base = project / "runs" / "executions"
    profile = get_data_profile(profile_name)
    return base / profile.name


def aggregate_output_path(project: Path, profile_name: str) -> Path:
    # Each profile gets its own default aggregate CSV so the two cohorts stay separate.
    profile = get_data_profile(profile_name)
    return project / profile.aggregate_csv_name
