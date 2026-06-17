# Gap analysis — ASHRAE HOF 2025 & EPW ↔ Climate Information schema

How the ASHRAE *Handbook of Fundamentals 2025* design-conditions spreadsheet
(`HOF_2025_Climate_Design_Conditions_SI.xlsx`, single `Stations` sheet, 588 columns,
header rows 1–4) and the EnergyPlus Weather (`.epw`) format map onto
`schema/ClimateInformation.schema.yaml` and the worked examples in `examples/`.

This revision (2026-06-17) reflects the expanded schema. The earlier draft listed many
ASHRAE quantities as *missing* from the YAML; almost all of those were added in the
2026-06-12 schema update, so **the YAML and the curated JSON example now describe the
same set of summary variables** (verified programmatically — see Part 1.3). What remains
are a handful of *structural* YAML↔JSON inconsistencies, called out in Part 1.4.

> Companion: `docs/implementation_and_application_notes.md` explains the data model,
> the unit conventions, and the full list of deliberate exclusions (its §4). This
> document is the column-level cross-check.

---

## Part 1 — ASHRAE design data ↔ schema

### 1.1 Station information (cols A–O) → `location`

| ASHRAE (col) | Schema | Note |
|---|---|---|
| Region (A) | `wmo_region` (1–6) | |
| Country / Prov State / Station Name (B/C/D) | `country_code` / `subdivision` / `name` | |
| WMO (E) / WBAN (F) | `wmo_station_id` / `wban_station_id` | the ASHRAE 6-digit WMO `725300` is now used everywhere for Chicago (the curated draft previously had `72530`). The `wigos_station_id` keeps the 5-digit traditional WMO, which is the correct WIGOS form. |
| Lat / Lon / Elev (G/H/I) | `latitude` / `longitude` / `elevation` | the onebuilding EPW/DDY report Chicago elevation as 201.8 m; the generators apply the ASHRAE **205 m** as a canonical override so every Chicago artifact agrees. |
| TZ Offset (K) | `time_zone_offset` | |
| Period / Climate Zone / Grade (M/N/O) | `SourceDataPeriod` / `climate_zones` / `SourceDataPeriod.ashrae_grade` | |
| StdP (J) | — | *excluded — derived from elevation (HOF Ch. 1)* |
| TZ Code (L) | `iana_time_zone_code` instead | the IANA code is stored in place of the ASHRAE `NAC`/`EUW` code |

### 1.2 Design conditions & climate normals → `summary_data`

Every ASHRAE design-conditions block now has a schema home. The mapping below is the
authoritative column-range cross-check (the schema variable names are the
`ClimateSummaryData` members).

| ASHRAE section (cols) | Schema variable(s) |
|---|---|
| Coldest / Hottest Month (P / AF) | `coldest_month` / `hottest_month` |
| Heating DB 99.6/99 (Q/R) + Cooling DB 0.4/1/2 (AH/AJ/AL) | `dry_bulb_temperature.annual.percent_exceedance` |
| Cooling MCWB (AI/AK/AM) | `dry_bulb_temperature_coincident_mean_wet_bulb_temperature` |
| Humidification DP 99.6/99 (S/V) + Dehumidification DP 0.4/1/2 (AV/AY/BB) | `dew_point_temperature.annual.percent_exceedance` |
| Humidification/Dehumidification MCDB (U/X, AX/BA/BD) | `dew_point_temperature_coincident_mean_dry_bulb_temperature` |
| Humidification/Dehumidification HR (T/W, AW/AZ/BC) | — *excluded — derivable from DP + station pressure* |
| Coldest-Month WS 0.4/1 (Y/AA) | — *the design WS itself is not stored; its MCDB is* |
| Coldest-Month WS MCDB (Z/AB) | `wind_speed_coincident_mean_dry_bulb_temperature` |
| MCWS to 99.6%/0.4% DB (AC/AT) | `dry_bulb_temperature_coincident_mean_wind_speed` |
| PCWD to 99.6%/0.4% DB (AD/AU) | `dry_bulb_temperature_coincident_prevailing_wind_direction` (radians) |
| Wind Shelter Factor (AE) | — *excluded — obsolete* |
| Hottest Month DB Range (AG) | = `daily_dry_bulb_temperature_range` at the hottest month (not stored separately) |
| Evaporation WB 0.4/1/2 (AN/AP/AR) | `wet_bulb_temperature.annual.percent_exceedance` |
| Evaporation MCDB (AO/AQ/AS) | `wet_bulb_temperature_coincident_mean_dry_bulb_temperature` |
| Enthalpy 0.4/1/2 (BE/BG/BI) | `enthalpy.annual.percent_exceedance` |
| Enthalpy MCDB (BF/BH/BJ) | `enthalpy_coincident_mean_dry_bulb_temperature` |
| Extreme Max WB (BK) | `wet_bulb_temperature.annual.maximum` |
| Extreme Annual WS 1/2.5/5 (BL–BN) | `wind_speed.annual.percent_exceedance` |
| Extreme Annual DB mean/std min&max (BO–BR) | `dry_bulb_temperature.annual.{mean,standard_deviation}_{minimum,maximum}` |
| Extreme Annual WB mean/std min&max (CA–CD) | `wet_bulb_temperature.annual.{mean,standard_deviation}_{minimum,maximum}` |
| n-Year Return Period Extreme DB / WB (BS–BZ, CE–CL) | — *excluded — derivable from extreme-annual mean/std* |
| Average Daily Temperature + its Std (CM–DL) | `daily_average_dry_bulb_temperature` (annual + monthly mean/std) |
| HDD/CDD 10 °C & 18.3 °C (DM–FL) | `heating_degree_days` / `cooling_degree_days` (two base temperatures) |
| Average Wind Speed annual+monthly (FM–FY) | `wind_speed.{annual,monthly}.mean` |
| Average / Max / Min / Std Precipitation (FZ–HY) | `liquid_precipitation_depth.{mean, maximum, minimum, standard_deviation}` |
| Monthly Design DB 0.4/2/5/10 + MCWB (HZ–LQ) | `dry_bulb_temperature.monthly` / `..._coincident_mean_wet_bulb_temperature.monthly` |
| Monthly Design WB 0.4/2/5/10 + MCDB (LR–PI) | `wet_bulb_temperature.monthly` / `..._coincident_mean_dry_bulb_temperature.monthly` |
| Mean Daily DB Range (PJ–PU) | `daily_dry_bulb_temperature_range` |
| Mean Daily DB/WB Range @ 5% design DB/WB (PV–RQ) | `daily_{dry,wet}_bulb_temperature_range_at_design_{dry,wet}_bulb_temperature` |
| Clear-Sky taub / taud (RR–SO) | `clear_sky_beam_optical_depth` / `clear_sky_diffuse_optical_depth` |
| Clear-Sky Noon Beam / Diffuse Irradiance, 21st (SP–TM) | — *excluded — derivable from taub/taud (HOF Ch. 14)* |
| All-Sky Avg + Std Monthly GHI (TN–UK) | `daily_all_sky_solar_irradiation` (mean + standard_deviation) |
| Historical Trends / Variability / Neighbors (UL–VP) | — *excluded — out of scope for the base model* |

### 1.3 YAML ↔ JSON variable parity

Comparing the YAML `ClimateSummaryData` data elements against the curated
`examples/USA_IL_Chicago-v2.1-draft.json` `summary_data`:

- **In JSON but not YAML:** *(none)*.
- **In YAML but not JSON:** `relative_humidity` only — defined as a summary variable but
  unused, because the ASHRAE design data has no summary relative-humidity column. This is
  intentional and harmless (a provider *may* publish it).

So the two are aligned: the schema defines exactly the variables the example uses, plus
`relative_humidity` in reserve.

### 1.4 Remaining YAML ↔ JSON inconsistencies (to resolve)

These are *structural* mismatches between the YAML definitions and the JSON examples —
not missing variables. They are the same open questions tracked in the companion notes
(§6); listed here with their concrete locations.

1. **`monthly` shape.** YAML `SummaryData.monthly` is `Array(Group(Statistics))` (an
   array of 12 `Statistics` objects); the JSON uses the compact object-of-arrays form
   (`monthly: { "mean": [12], … }`). Pick one and align the other.
2. **`DegreeDays` vs `DegreeDay`.** `ClimateSummaryData.heating_degree_days` /
   `cooling_degree_days` are typed `Array(Group(DegreeDays))`, but the defined group is
   `DegreeDay` (singular) — `DegreeDays` is undefined.
3. **`SummaryDataSet.climate_data_type`.** The JSON sets `climate_data_type`
   (MEASURED/MODELED) at the data-set level, but the YAML `SummaryDataSet` group only
   defines `source_data_periods`, `summary_data`, `notes`. (Per-variable
   `SummaryData.source_data_type` *is* defined and is what the generated examples use.)
4. **`metadata` has no group.** `ClimateInformation.metadata` is typed `Group(Metadata)`,
   but no `Metadata` group is defined anywhere in the YAML.
5. **`ashrae_grade` constraint syntax.** `SourceDataPeriod.ashrae_grade` uses
   `Constraints: '["A", "B", "C", "D", "E"]'`, which `lattice` cannot parse — the schema
   currently fails to compile, so JSON-Schema validation of the examples is unavailable
   until this is fixed.
6. **Coincident / monthly percent-exceedance shape.** `PercentTimeExceedanceCoincident`
   is malformed (its `grid_variables` nests a `percent_time_exceeded` element instead of
   referencing `PercentTimeExceedanceGridVariables`), and the JSON's *monthly*
   `percent_exceedance` (`[{percent_time_exceeded, values:[12]}]`) matches neither
   percent-exceedance group. The *annual* grid/lookup form is consistent.
7. **Time-series data-set shape.** YAML `TimeSeriesDataSet` uses `time_intervals`
   (array of `TimeInterval`) + a `time_series` group; the curated draft used a singular
   `source_data_period` with variables inline. The EPW-generated examples
   (`examples/generated/*-from-epw.v2.1.json`) follow the **YAML** shape.

---

## Part 2 — EPW ↔ schema

An EPW file contributes a `LOCATION` line, an optional `DESIGN CONDITIONS` line and 8760
hourly records. `tools/epw_to_json.py` performs this mapping, and `tools/json_to_epw.py`
performs the reverse (likewise `ddy_to_json.py` / `json_to_ddy.py` for DDY). The mapping
is the same in both directions; the round-trip is verified by the test suite.

### 2.1 `LOCATION` line → `location`

`LOCATION, City, State, Country, Source, WMO, Lat, Lon, TZ, Elevation`

| EPW field | Schema |
|---|---|
| City / State / Country | `name` / `subdivision` / `country_code` |
| WMO | `wmo_station_id` |
| Lat / Lon / TZ / Elevation | `latitude` / `longitude` / `time_zone_offset` / `elevation` |
| *(none)* | `iana_time_zone_code` — **EPW has no IANA code**; inferred as `Etc/GMT±N` from the offset |
| *(none)* | `anemometer_height` (10 m) / `station_height` (1.8 m) — assumed |

### 2.2 `DESIGN CONDITIONS` line → `summary_data`

The EPW `DESIGN CONDITIONS` line is the ASHRAE spreadsheet columns **P–CL laid end to
end** in three labelled sections (`Heating` = P–AE, `Cooling` = AF–BK, `Extremes` =
BL–CL). It maps to the **annual** design conditions exactly as in Part 1.2 (verified:
the EPW-derived `percent_exceedance` grids and extreme-annual statistics reproduce the
curated draft's annual blocks value-for-value; the annual `mean`/`standard_deviation`
are *not* in the header — they come from columns CM+, below).
Everything from spreadsheet column CM onward (average daily temperature, degree days,
average/monthly wind speed, precipitation, monthly design DB/WB, mean daily ranges,
clear-sky/all-sky solar) is **not** in the EPW header — it lives in the `.stat` file —
so those `ClimateSummaryData` variables are absent from an EPW-derived summary.

### 2.3 Hourly records (35 fields) → `time_series`

| EPW field (index) | Schema `ClimateTimeSeries` variable | Conversion to base SI |
|---|---|---|
| Dry-bulb temperature (6) | `dry_bulb_temperature` | °C → K |
| Dew-point temperature (7) | `dew_point_temperature` | °C → K |
| Relative humidity (8) | `relative_humidity` | % → fraction |
| Atmospheric pressure (9) | `atmospheric_pressure` | Pa (as-is) |
| Horizontal IR sky (12) | `horizontal_infrared_sky_irradiance` | Wh/m²·h ≈ W/m² |
| Global horizontal radiation (13) | `global_horizontal_irradiation` (SUM) | Wh/m² → J/m² (×3600) |
| Direct normal radiation (14) | `direct_normal_irradiation` (SUM) | Wh/m² → J/m² |
| Diffuse horizontal radiation (15) | `diffuse_horizontal_irradiation` (SUM) | Wh/m² → J/m² |
| Global/Direct/Diffuse illuminance (16/17/18) | `*_illuminance` | lux (as-is) |
| Wind direction (20) | `wind_direction` | degrees → radians |
| Wind speed (21) | `wind_speed` | m/s (as-is) |
| Total / Opaque sky cover (22/23) | `total_sky_cover` / `opaque_sky_cover` | tenths → fraction |
| Precipitable water (28) | `precipitable_water` | mm → m |
| Aerosol optical depth (29) | `aerosol_optical_depth` | unitless |
| Snow depth (30) | `snow_depth` | cm → m |
| Albedo (32) | `albedo` | unitless |
| Liquid precipitation depth (33) | `liquid_precipitation_depth` (SUM) | mm → m |

> EPW reports radiation as energy received over the hour (Wh/m²), so it maps to the
> schema's *irradiation* (`J/m²`, `value_type=SUM`) variables rather than the
> instantaneous *irradiance* (`W/m²`) ones.

**EPW fields with no schema home:** Year/Month/Day/Hour/Minute (encoded in the
`TimeInterval` instead), the data-source/uncertainty flag string, extraterrestrial
horizontal & direct-normal radiation (10/11), zenith luminance (19), visibility (24),
ceiling height (25), present-weather observation & codes (26/27), days since last
snowfall (31), and liquid-precipitation quantity/hours (34).

**Schema time-series variables not in the EPW:** `wet_bulb_temperature`,
`humidity_ratio`, the instantaneous irradiance forms
(`global/direct/diffuse_*_irradiance`), `sky_type`, and the whole air-quality /
pollutant set (`particulate_matter_*`, `carbon_dioxide`, `nitrogen_dioxide`,
`nitrogen_oxide`, `sulphur_dioxide`, `ozone`, `ammonia`, `carbon_monoxide`,
`formaldehyde`, `benzene`, `voc`, `turbidity`, `lead`, `mercury`).

### 2.4 Missing values: EPW sentinels ↔ schema `null`

EPW has no blank/missing concept — every field carries a numeric sentinel (99.9 °C for
temperature, 999 for %/direction/speed, 9999 for Wh/m², 999999 for pressure/illuminance,
etc.). The v2.1 schema supports an explicit `null`, so on import (`epw_to_json.py`) each
sentinel becomes `null` and on export (`json_to_epw.py`) each `null` returns to the
sentinel. This is exercised by
`tools/test_climate_helpers.py::test_null_roundtrip_epw_json` (and is the round-trip
illustrated by `extra_examples/test_20251017.json`).

When the reverse converter re-emits an EPW, quantities the model deliberately drops
(humidity ratio, wind shelter factor, n-year return periods) come back blank, and EPW
fields with no schema home (extraterrestrial radiation, zenith luminance, visibility,
ceiling height, present weather, days-since-snow, liquid-precipitation hours) come back
as their sentinels — see §2.3. The modeled data round-trips exactly.
