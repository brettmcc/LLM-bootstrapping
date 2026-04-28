"""Helpers for switching between the legacy and expanded ACS extracts."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


LEGACY_DATA_PROFILE = "legacy"
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
    LEGACY_DATA_PROFILE: DataProfile(
        name=LEGACY_DATA_PROFILE,
        description="Legacy ACS extract based on usa_00042.",
        data_file_name="usa_00042.dat",
        layout_file_name="usa_00042.do",
        run_data_file_name="usa_00042.dat",
        run_layout_excerpt_name="usa_00042_layout_excerpt.do",
        aggregate_csv_name="runs_complete.csv",
    ),
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


def data_profile_choices() -> tuple[str, ...]:
    # argparse wants a stable iterable of allowed profile names.
    return tuple(DATA_PROFILES)


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
    # Legacy specs stay in the historical location; expanded specs live under an explicit subfolder.
    base = project / "specs"
    if phase12:
        base = base / "phase12"
    profile = get_data_profile(profile_name)
    if profile.name == LEGACY_DATA_PROFILE:
        return base
    return base / profile.name


def specs_dir(project: Path, provider: str, profile_name: str, *, phase12: bool = False) -> Path:
    # Provider-specific spec directory for the selected data profile.
    return specs_base_dir(project, profile_name, phase12=phase12) / provider


def conversations_root(project: Path, profile_name: str) -> Path:
    # Keep legacy API logs in the existing root; expanded logs get their own namespace.
    base = project / "runs" / "conversations"
    profile = get_data_profile(profile_name)
    if profile.name == LEGACY_DATA_PROFILE:
        return base
    return base / profile.name


def conversations_dir(project: Path, model_dir: str, profile_name: str) -> Path:
    # Raw Phase 1 API logs are grouped by model inside the profile-specific root.
    return conversations_root(project, profile_name) / model_dir


def executions_root(project: Path, profile_name: str, *, phase12: bool = False) -> Path:
    # Legacy execution runs stay where they are; expanded runs live under dedicated subfolders.
    base = project / "runs" / "executions"
    if phase12:
        base = base / "phase12"
    profile = get_data_profile(profile_name)
    if profile.name == LEGACY_DATA_PROFILE:
        return base
    return base / profile.name


def aggregate_output_path(project: Path, profile_name: str) -> Path:
    # Each profile gets its own default aggregate CSV so the two cohorts stay separate.
    profile = get_data_profile(profile_name)
    return project / profile.aggregate_csv_name