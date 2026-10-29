# GeoXVIEW data

License: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Please cite the archive DOI 10.26153/tsw/64936.

All values are summaries per field site or per map unit. They are the same values shown in the public dashboard. Units (as labeled in the dashboard): temperatures in °F, PM2.5 and PM10 in µg/m³, VOC in ppm, relative humidity in %, wind in m/s.

## Files

| File | Rows | One row per |
|---|---|---|
| `sites.csv` | 1,400 | field site |
| `sites_seasonal.csv` | 5,600 | site and season |
| `site_scales.csv` | 6,917 | site and map unit that contains it |
| `boundaries/eei_boundaries.gpkg` | 28,642 | polygon; one layer per scale: `county`, `subdivision`, `zip`, `tract`, `blockgroup` |
| `boundaries/texas_outline.geojson` | 1 | Texas outline |

## `sites.csv` columns

| Column | Meaning |
|---|---|
| `id` | Site ID (GV-0001 to GV-1400). Some sites share coordinates (several measurement points at one location). |
| `lat`, `lon` | WGS84 coordinates |
| `place`, `county`, `fips` | Site name, county name, county FIPS code |
| `nlcd`, `ecoregion`, `koppen`, `urban` | Sampling strata: NLCD land cover class, EPA Level III ecoregion, Köppen climate zone, urban class |
| `aqi_norm`, `lst_norm`, `lulc_norm` | EEI components, each normalized to 0 to 100 |
| `eei` | Environmental Exposure Index = mean of the three components |
| `eei_class` | Low (< 35), Moderate (35 to < 50), High (50 to < 65), Very High (≥ 65) |
| `eei_peak`, `eei_trough`, `eei_std`, `eei_seasons` | Highest, lowest and standard deviation of seasonal EEI; number of seasonal records (16 for every site) |
| `maup_spread` | Highest minus lowest unit mean EEI across the five map units |
| `maup_n_cats` | Number of different EEI classes across the five map units |
| `thermal_*` | Air temperature, sunlit and shaded surface temperature, vegetation temperature (°F); `warm_rat` = sunlit/shaded ratio |
| `airq_*` | Air quality monitor: temperature (°F), VOC (ppm), PM2.5 and PM10 (µg/m³), air quality score |
| `weather_*` | Relative humidity (%), wind (m/s), heat index (°F), dew point (°F) |
| `landcover_*` | Share of impervious, tree, developed, natural and agricultural cover around the site (%) |
| `gsv_*` | Street-view and built-environment features: brightness, green, sky and edge ratios, road and building density, points of interest, green space, transit, water, enclosure, shade and sidewalk scores |

## `site_scales.csv` columns

`id`, `scale`, `unit_id` (GEOID or ZIP), `unit_name`, `n_sites` (measured sites in the unit), `mean_eei`, `eei_class`.

## Boundary layers

Each polygon has `unit_id`, `unit_name`, `eei`, `eei_class`, `n_sites`, `status`, `ecoregion`, `koppen`.
`status = measured` means the unit holds at least one field site. `status = estimated` means its value comes from sites in the same ecoregion and climate stratum (spatial proxy), not from a site inside it. Treat estimated values as screening values only.

## Not included

Raw instrument logs, thermal images, photos and resident survey responses. Survey data are covered by a UT Austin IRB protocol.
