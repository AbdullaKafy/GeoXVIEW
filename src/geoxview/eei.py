"""Environmental Exposure Index (EEI).

The EEI combines three normalized components (0 to 100 each):
air quality (`aqi_norm`), land surface temperature (`lst_norm`) and
land use / land cover (`lulc_norm`). The published index is their
equal-weight mean. Each component is also kept separately, so a high
value in one component is never hidden by a low value in another.
"""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
import pandas as pd

COMPONENTS = ("aqi_norm", "lst_norm", "lulc_norm")

# Class limits used in the GeoXVIEW dashboard.
EEI_BREAKS = (35.0, 50.0, 65.0)
EEI_CLASSES = ("Low", "Moderate", "High", "Very High")


def compute_eei(
    df: pd.DataFrame,
    weights: Sequence[float] | None = None,
    components: Sequence[str] = COMPONENTS,
) -> pd.Series:
    """Weighted mean of the components. Default is equal weights."""
    w = np.ones(len(components)) if weights is None else np.asarray(weights, dtype=float)
    if w.shape != (len(components),) or np.any(w < 0) or w.sum() == 0:
        raise ValueError("weights must be non-negative, one per component, and not all zero")
    w = w / w.sum()
    return pd.Series(df[list(components)].to_numpy() @ w, index=df.index, name="eei")


def classify_eei(values, breaks: Sequence[float] = EEI_BREAKS) -> pd.Series:
    """Map EEI values to Low / Moderate / High / Very High."""
    values = pd.Series(values)
    idx = np.searchsorted(np.asarray(breaks), values.to_numpy(), side="right")
    return pd.Series(np.asarray(EEI_CLASSES)[idx], index=values.index, name="eei_class")


def weight_sensitivity(
    df: pd.DataFrame,
    n_draws: int = 500,
    concentration: float = 5.0,
    seed: int = 0,
    components: Sequence[str] = COMPONENTS,
) -> pd.DataFrame:
    """How stable are site ranks and classes when the weights change?

    Draws random weights around equal weights (Dirichlet distribution;
    a larger `concentration` keeps weights closer to equal). For each draw it
    reports the Spearman rank correlation with the equal-weight EEI and the
    share of sites whose class changes.
    """
    rng = np.random.default_rng(seed)
    base = compute_eei(df, components=components)
    base_rank = base.rank()
    base_cls = classify_eei(base)
    rows = []
    for w in rng.dirichlet(np.full(len(components), concentration), size=n_draws):
        e = compute_eei(df, weights=w, components=components)
        rows.append(
            {
                **{f"w_{c}": wi for c, wi in zip(components, w, strict=True)},
                "spearman": float(np.corrcoef(base_rank, e.rank())[0, 1]),
                "class_change_share": float((classify_eei(e) != base_cls).mean()),
            }
        )
    return pd.DataFrame(rows)
