# Changelog

Notable changes to the Climate Information data model
(`schema/ClimateInformation.schema.yaml`) and the artifacts generated from it.

## Unreleased -- schema `Version: 0.2.0` (the "v2.1 draft" examples)

### From time series to summaries

The data model began as a time-series weather model: the `ClimateTimeSeries` variable set
(temperature, humidity, the solar irradiance/irradiation family, wind, sky cover,
precipitation, and a broad air-quality/pollutant list) describes an hourly or sub-hourly
record for a station. That side is mature and is unchanged.

This version adds the summary / design-data side -- the `ClimateSummaryData` and
`Statistics` groups -- so the same document can carry both the raw record and the
statistical and design summaries derived from it.

### Added

- `location.wmo_region` (Integer 1-6).
- `Statistics.maximum` and `Statistics.minimum` (single observed extremes).
- New `ClimateSummaryData` variables:
  - `wet_bulb_temperature`, `wind_speed`, `enthalpy`.
  - The coincident variables
    `dew_point_temperature_coincident_mean_dry_bulb_temperature`,
    `wet_bulb_temperature_coincident_mean_dry_bulb_temperature`,
    `dry_bulb_temperature_coincident_prevailing_wind_direction`,
    `enthalpy_coincident_mean_dry_bulb_temperature`,
    `wind_speed_coincident_mean_dry_bulb_temperature`.
  - `clear_sky_beam_optical_depth`, `clear_sky_diffuse_optical_depth`,
    `daily_all_sky_solar_irradiation`.
  - The five `daily_*_temperature_range*` variables.
  - The `coldest_month` / `hottest_month` convenience indices.

### Removed

Nothing. Time-series variables already present but outside any design table (for example
the air-quality and illuminance variables) were left in place.

### Examples

- `examples/curated/USA_IL_Chicago-v2.1-draft.json` -- a full summary for Chicago O'Hare
  (WMO 725300).
- `examples/curated/GBR_Scotland_Glasgow-Bishopton-v2.1-draft.json` -- Glasgow Bishopton
  (WMO 03134).
- `examples/generated/` -- EPW/DDY <-> JSON round-trips produced by the `tools/`
  converters.
- `examples/curated/USA_IL_Chicago-v1.json` predates this schema entirely (2021) and is
  excluded from validation pending a real migration
  (IBPSA-USA/climate-information#8).
