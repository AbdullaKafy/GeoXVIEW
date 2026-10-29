"""GeoXVIEW: scale-adaptive environmental exposure modeling for Texas.

Main parts:
- io: load the field-site table and the boundary layers.
- eei: build and classify the Environmental Exposure Index (EEI).
- maup: measure how much a site's exposure class changes with the map unit.
- validation: spatial block cross-validation for any scikit-learn model.
"""

from geoxview.eei import COMPONENTS, EEI_CLASSES, classify_eei, compute_eei, weight_sensitivity
from geoxview.io import load_boundaries, load_seasonal, load_site_scales, load_sites
from geoxview.maup import class_agreement, scale_spread
from geoxview.validation import compare_cv, spatial_block_cv

__version__ = "0.1.0"

__all__ = [
    "COMPONENTS",
    "EEI_CLASSES",
    "class_agreement",
    "classify_eei",
    "compare_cv",
    "compute_eei",
    "load_boundaries",
    "load_seasonal",
    "load_site_scales",
    "load_sites",
    "scale_spread",
    "spatial_block_cv",
    "weight_sensitivity",
]
