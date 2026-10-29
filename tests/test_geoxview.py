"""Tests: the package must reproduce the values published in the dashboard."""

import numpy as np
import pandas as pd
import pytest
from sklearn.linear_model import LinearRegression

import geoxview as gx
from geoxview.validation import grid_blocks


@pytest.fixture(scope="module")
def sites():
    return gx.load_sites()


@pytest.fixture(scope="module")
def site_scales():
    return gx.load_site_scales()


def test_site_table_shape(sites):
    assert len(sites) == 1400
    assert sites["id"].is_unique
    assert sites["fips"].nunique() == 254  # every Texas county
    assert sites["nlcd"].nunique() == 15
    assert sites["ecoregion"].nunique() == 12
    assert sites["koppen"].nunique() == 5


def test_eei_is_equal_weight_mean(sites):
    eei = gx.compute_eei(sites)
    # published values are rounded to one decimal place
    assert np.abs(eei - sites["eei"]).max() < 0.1


def test_eei_classes_match_published(sites):
    assert (gx.classify_eei(sites["eei"]) == sites["eei_class"]).all()


def test_class_breaks():
    got = gx.classify_eei([10, 35, 49.9, 50, 64.9, 65, 90]).tolist()
    assert got == ["Low", "Moderate", "Moderate", "High", "High", "Very High", "Very High"]


def test_bad_weights_rejected(sites):
    with pytest.raises(ValueError):
        gx.compute_eei(sites, weights=[1, -1, 1])
    with pytest.raises(ValueError):
        gx.compute_eei(sites, weights=[1, 1])


def test_scale_spread_matches_published(sites, site_scales):
    sp = gx.scale_spread(site_scales)
    pub = sites.set_index("id").loc[sp.index]
    assert np.allclose(sp["spread"], pub["maup_spread"], atol=1e-9)
    assert (sp["n_classes"] == pub["maup_n_cats"]).all()


def test_class_agreement_is_a_share(site_scales):
    agree = gx.class_agreement(site_scales)
    assert len(agree) == 10  # 5 scales -> 10 pairs
    assert agree["same_class_share"].between(0, 1).all()


def test_weight_sensitivity_columns(sites):
    out = gx.weight_sensitivity(sites, n_draws=20)
    assert {"spearman", "class_change_share"} <= set(out.columns)
    assert out["spearman"].between(-1, 1).all()


def test_spatial_cv_holds_blocks_out():
    rng = np.random.default_rng(1)
    lat = rng.uniform(26, 36, 400)
    lon = rng.uniform(-106, -94, 400)
    X = np.c_[lat, lon]
    y = 2 * lat + rng.normal(0, 1, 400)
    res = gx.spatial_block_cv(LinearRegression(), X, y, lat, lon, block_km=100)
    assert len(res) == 5 and res["r2"].mean() > 0.5
    blocks = grid_blocks(lat, lon, 100)
    assert len(np.unique(blocks)) > 5


def test_compare_cv_returns_both_schemes():
    rng = np.random.default_rng(2)
    lat, lon = rng.uniform(26, 36, 300), rng.uniform(-106, -94, 300)
    X = pd.DataFrame({"a": lat, "b": lon})
    out = gx.compare_cv(LinearRegression(), X, lat + rng.normal(0, 1, 300), lat, lon)
    assert out.shape == (2, 2)
