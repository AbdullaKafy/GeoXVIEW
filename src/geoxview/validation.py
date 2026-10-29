"""Spatial block cross-validation.

Random cross-validation lets nearby, similar sites fall in both the
training and the test fold. Scores then look better than the model really
is. Spatial block cross-validation puts sites into grid blocks and keeps
each whole block in one fold, so the model is always tested on places it
has not seen nearby.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import GroupKFold, KFold


def grid_blocks(lat, lon, block_km: float = 50.0) -> np.ndarray:
    """Assign each point to a square grid block of about `block_km` km."""
    lat = np.asarray(lat, dtype=float)
    lon = np.asarray(lon, dtype=float)
    dlat = block_km / 111.0
    dlon = block_km / (111.0 * np.cos(np.deg2rad(np.nanmean(lat))))
    row = np.floor(lat / dlat).astype(int)
    col = np.floor(lon / dlon).astype(int)
    return row * 100_000 + col


def _score(model, X, y, splits):
    rows = []
    for k, (tr, te) in enumerate(splits):
        m = clone(model).fit(X[tr], y[tr])
        p = m.predict(X[te])
        rows.append(
            {
                "fold": k,
                "r2": r2_score(y[te], p),
                "rmse": float(np.sqrt(mean_squared_error(y[te], p))),
                "n_test": len(te),
            }
        )
    return pd.DataFrame(rows)


def spatial_block_cv(model, X, y, lat, lon, block_km: float = 50.0, n_splits: int = 5):
    """Fold scores with whole spatial blocks held out together."""
    X, y = np.asarray(X), np.asarray(y)
    groups = grid_blocks(lat, lon, block_km)
    splits = GroupKFold(n_splits=n_splits).split(X, y, groups)
    return _score(model, X, y, splits)


def random_cv(model, X, y, n_splits: int = 5, seed: int = 0):
    """Ordinary shuffled K-fold, for comparison."""
    X, y = np.asarray(X), np.asarray(y)
    splits = KFold(n_splits=n_splits, shuffle=True, random_state=seed).split(X)
    return _score(model, X, y, splits)


def compare_cv(model, X, y, lat, lon, block_km: float = 50.0, n_splits: int = 5) -> pd.DataFrame:
    """Mean R2 and RMSE for random and spatial block CV side by side."""
    r = random_cv(model, X, y, n_splits).assign(scheme="random")
    s = spatial_block_cv(model, X, y, lat, lon, block_km, n_splits).assign(
        scheme=f"spatial block ({block_km:g} km)"
    )
    return pd.concat([r, s]).groupby("scheme", sort=False)[["r2", "rmse"]].mean()
