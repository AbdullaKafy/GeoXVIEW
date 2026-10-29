"""Load GeoXVIEW data files.

All loaders look in the repository `data/` folder by default.
You can pass another folder with `data_dir`.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

SCALES = ("county", "subdivision", "zip", "tract", "blockgroup")


def _data_dir(data_dir: str | Path | None) -> Path:
    if data_dir is not None:
        return Path(data_dir)
    # src/geoxview/io.py -> repository root -> data
    return Path(__file__).resolve().parents[2] / "data"


def load_sites(data_dir: str | Path | None = None) -> pd.DataFrame:
    """One row per field site (1,400 rows) with mean values and EEI."""
    return pd.read_csv(_data_dir(data_dir) / "sites.csv", dtype={"fips": str})


def load_seasonal(data_dir: str | Path | None = None) -> pd.DataFrame:
    """One row per site and season with seasonal mean readings."""
    return pd.read_csv(_data_dir(data_dir) / "sites_seasonal.csv")


def load_site_scales(data_dir: str | Path | None = None) -> pd.DataFrame:
    """One row per site and boundary scale.

    `mean_eei` is the mean EEI of all measured sites inside the unit
    (county, county subdivision, ZIP code, census tract or block group)
    that contains the site.
    """
    return pd.read_csv(_data_dir(data_dir) / "site_scales.csv", dtype={"unit_id": str})


def load_boundaries(scale: str, data_dir: str | Path | None = None):
    """Boundary polygons with EEI for one scale. Needs geopandas.

    `status` is "measured" when the unit holds at least one field site,
    and "estimated" when its value comes from a stratum-matched proxy.
    """
    if scale not in SCALES:
        raise ValueError(f"scale must be one of {SCALES}, got {scale!r}")
    try:
        import geopandas as gpd
    except ImportError as err:  # pragma: no cover
        raise ImportError("load_boundaries needs geopandas: pip install geoxview[geo]") from err
    path = _data_dir(data_dir) / "boundaries" / "eei_boundaries.gpkg"
    return gpd.read_file(path, layer=scale)
