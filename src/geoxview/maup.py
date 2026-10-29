"""Modifiable areal unit problem (MAUP) diagnostics.

The same field site sits inside a county, a county subdivision, a ZIP code,
a census tract and a block group. Each unit reports its own mean EEI.
These functions show how much the reported exposure for one place depends
on which unit is used.
"""

from __future__ import annotations

from itertools import combinations

import pandas as pd

from geoxview.io import SCALES


def scale_spread(site_scales: pd.DataFrame) -> pd.DataFrame:
    """Per site: range of unit EEI across scales and number of distinct classes.

    `spread` = highest minus lowest unit mean EEI across the available scales.
    `n_classes` > 1 means the site's exposure class changes with the map unit.
    """
    g = site_scales.groupby("id")
    out = pd.DataFrame(
        {
            "spread": g["mean_eei"].max() - g["mean_eei"].min(),
            "n_classes": g["eei_class"].nunique(),
            "n_scales": g["scale"].nunique(),
        }
    )
    out["class_changes"] = out["n_classes"] > 1
    return out


def class_agreement(site_scales: pd.DataFrame, scales=SCALES) -> pd.DataFrame:
    """Share of sites that keep the same EEI class between every pair of scales."""
    wide = site_scales.pivot(index="id", columns="scale", values="eei_class")
    rows = []
    for a, b in combinations([s for s in scales if s in wide.columns], 2):
        both = wide[[a, b]].dropna()
        rows.append(
            {
                "scale_a": a,
                "scale_b": b,
                "n_sites": len(both),
                "same_class_share": float((both[a] == both[b]).mean()),
            }
        )
    return pd.DataFrame(rows)
