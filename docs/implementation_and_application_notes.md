# Climate Information Data Model — Implementation & Application Notes

A companion to `schema/ClimateInformation.schema.yaml` and the worked examples in
`examples/`. It explains how the data model is structured, how the ASHRAE Handbook
of Fundamentals (HOF) 2025 design-conditions data maps onto it, which ASHRAE
quantities are **deliberately excluded** and why, and the open design questions that
still need resolving.

> This is a *companion / design* document. The normative definition is the schema
> YAML; the published specification is generated from it (see `docs/`). For the raw
> running list of committee questions and decisions, see
> `extra_examples/notes_with_json_example.cleaned.md`. The canonical list of
> deliberate exclusions now lives in this document (§4).

---

## 1. How the model is structured

A climate-information document is a single JSON object with four top-level members
(`ClimateInformation` in the schema):

| Member | Purpose |
|---|---|
| `metadata` | Document-level provenance: schema id/version, description, timestamps, copyright/licence. |
| `location` | The weather station: identifiers, coordinates, elevation, time zone, climate-zone classifications. |
| `summary_data_sets` | One or more **statistical summaries** of the climate (the ASHRAE-style design conditions live here). |
| `time_series_data_sets` | One or more **time series** (e.g. an hourly typical year). |

### 1.1 Summary data sets

Each `SummaryDataSet` carries:

- `source_data_periods` — an array of `SourceDataPeriod` (id, `start_time`,
  `end_time`, `notes`, `ashrae_grade`). Different variables can reference different
  periods — e.g. solar quantities typically use a shorter record than temperature.
- `summary_data` — a `ClimateSummaryData` group whose members are the climate
  variables (dry-bulb temperature, precipitation, degree days, …).

Every ordinary variable is a `SummaryData` group:

```jsonc
"dry_bulb_temperature": {
  "display_name": "Dry-bulb temperature",
  "units": "K",
  "source_data_period": "Handbook 2025 period of record",  // -> SourceDataPeriod.id
  "source_data_type": "MEASURED",                           // MEASURED | MODELED
  "annual":  { /* Statistics */ },
  "monthly": { /* 12 monthly Statistics */ }
}
```

### 1.2 The `Statistics` block — the heart of the model

Rather than hard-coding ASHRAE's specific percentiles as named fields (`Heating 99.6%`,
`Cooling 0.4%`, …), the model stores a generic distribution summary per variable:

- Central tendency / spread: `mean`, `standard_deviation`.
- Annual extremes: `mean_minimum`, `mean_maximum`,
  `standard_deviation_minimum`, `standard_deviation_maximum` — the mean and standard
  deviation of the per-year minima/maxima (this is exactly ASHRAE's *Extreme Annual*
  block).
- Single observed extremes: `maximum`, `minimum` (added for ASHRAE *Extreme Max WB*
  and *Max/Min Precipitation*).
- `percent_exceedance` — the design conditions, as a **grid + lookup** pair:

```jsonc
"percent_exceedance": {
  "grid_variables":   { "percent_time_exceeded": [0.4, 1.0, 2.0, 99.0, 99.6] },
  "lookup_variables": { "values":                [306.05, 304.65, 303.25, 257.85, 255.05] }
}
```

`values[i]` is the threshold the variable exceeds `percent_time_exceeded[i]` % of the
time. Low percentages (0.4/1/2) are the **cooling/hot** design conditions; high
percentages (99/99.6) are the **heating/cold** ones. Storing the percentiles as data
(not as schema keys) means a provider can publish any set of exceedance levels without
a schema change.

### 1.3 Coincident variables

ASHRAE pairs many design conditions with the *mean coincident* value of another
variable (MCWB, MCDB, MCWS, PCWD, …). These are modelled as **separate named
variables** following the convention
`<base>_coincident_<statistic>_<other>`:

| Model variable | ASHRAE quantity |
|---|---|
| `dry_bulb_temperature_coincident_mean_wet_bulb_temperature` | Cooling DB → MCWB |
| `dry_bulb_temperature_coincident_mean_wind_speed` | MCWS to 0.4%/99.6% DB |
| `dry_bulb_temperature_coincident_prevailing_wind_direction` | PCWD to 0.4%/99.6% DB |
| `wet_bulb_temperature_coincident_mean_dry_bulb_temperature` | Evaporation WB → MCDB |
| `dew_point_temperature_coincident_mean_dry_bulb_temperature` | Humidification/Dehumidification → MCDB |
| `enthalpy_coincident_mean_dry_bulb_temperature` | Enthalpy → MCDB |
| `wind_speed_coincident_mean_dry_bulb_temperature` | Coldest-month WS → MCDB |

For a coincident variable, `percent_time_exceeded` refers to the percentile **of the
base variable**, and `values` holds the coincident statistic at that percentile. For
example, `wet_bulb_temperature_coincident_mean_dry_bulb_temperature` at
`percent_time_exceeded = 0.4` is the mean DB observed when the WB is at its 0.4% design
value.

### 1.4 Degree days

`heating_degree_days` / `cooling_degree_days` are **arrays** of `DegreeDay` groups, one
per base temperature, each with `base_temperature` (K), `annual`, and optional
`monthly[12]`. The examples include the two ASHRAE bases: 10 °C = 283.15 K and
18.3 °C = 291.45 K.

### 1.5 Time series data sets

`TimeSeriesDataSet` holds `TimeInterval`s (regular interval or explicit timestamps) and
named `TimeSeries` variables that reference an interval by id, plus optional
`uncertainty`, `source`, and per-step `notes`. The example files include only a
skeleton (values omitted) — the focus of these examples is the summary/design data.

---

## 2. Units — everything is SI base

The schema is SI base throughout; the ASHRAE *SI* spreadsheet is **not** in base units,
so values are converted on import:

| Quantity | ASHRAE (SI sheet) | Model | Conversion |
|---|---|---|---|
| Temperature (absolute) | °C | K | `+ 273.15` |
| Temperature **range** / standard deviation | °C | K | identical value (it is a difference) |
| Degree-days | °C-day | K-day | identical value (a difference) |
| Precipitation depth | mm | m | `÷ 1000` |
| Enthalpy | kJ/kg | J/kg | `× 1000` |
| All-sky daily irradiation | kWh/m²/day | J/m² | `× 3.6 × 10⁶` |
| Wind direction | degrees | radians | `× π/180` |
| Wind speed | m/s | m/s | — |
| Optical depth (taub/taud) | — | — | dimensionless |

> Note the distinction between **absolute** temperatures (add 273.15) and temperature
> **ranges / standard deviations / degree-days** (a difference — the numeric value is
> the same in K and °C). Getting this wrong is the easiest mistake to make.

---

## 3. ASHRAE HOF 2025 coverage — what maps where

The ASHRAE design-conditions spreadsheet (`HOF_2025_Climate_Design_Conditions_SI.xlsx`,
single `Stations` sheet, 588 columns) is the source of truth for the variable list.
Below is how its sections map onto the model.

### 3.1 Station information (cols A–O) → `location`

| ASHRAE | Model | |
|---|---|---|
| Region | `wmo_region` | added |
| Country / Prov State / Station Name | `country_code` / `subdivision` / `name` | |
| WMO / WBAN | `wmo_station_id` / `wban_station_id` | |
| Lat / Lon / Elev | `latitude` / `longitude` / `elevation` | |
| TZ Offset | `time_zone_offset` | |
| Period / Climate Zone / Grade | `SourceDataPeriod` / `climate_zones` / `ashrae_grade` | |
| **StdP** | — | *excluded — derived from elevation (HOF Ch. 1)* |
| **TZ Code** | `iana_time_zone_code` instead | *the IANA code is stored in place of the ASHRAE code* |

### 3.2 Design conditions → `summary_data`

| ASHRAE section | Model representation |
|---|---|
| Heating DB (99.6/99.0), Cooling DB (0.4/1/2) | `dry_bulb_temperature.percent_exceedance` |
| Humidification DP (99.6/99.0), Dehumidification DP (0.4/1/2) | `dew_point_temperature.percent_exceedance` |
| Cooling MCWB | `dry_bulb_temperature_coincident_mean_wet_bulb_temperature` |
| Evaporation WB (0.4/1/2) | `wet_bulb_temperature.percent_exceedance` |
| Evaporation MCDB, Monthly-design-WB MCDB | `wet_bulb_temperature_coincident_mean_dry_bulb_temperature` |
| Humidification/Dehumidification MCDB | `dew_point_temperature_coincident_mean_dry_bulb_temperature` |
| Enthalpy (0.4/1/2) + MCDB | `enthalpy` + `enthalpy_coincident_mean_dry_bulb_temperature` |
| Extreme Max WB | `wet_bulb_temperature.annual.maximum` |
| Extreme Annual DB (mean/std of min/max) | `dry_bulb_temperature.annual.mean_minimum/…` |
| Extreme Annual WB (mean/std of min/max) | `wet_bulb_temperature.annual.mean_minimum/…` |
| MCWS / PCWD to 0.4%/99.6% DB | `…_coincident_mean_wind_speed` / `…_coincident_prevailing_wind_direction` |
| Average / Extreme Annual / Coldest-month wind speed | `wind_speed` (mean + percent_exceedance) |
| Coldest-month WS MCDB | `wind_speed_coincident_mean_dry_bulb_temperature` |
| Average Daily Temperature (+ its std) | `daily_average_dry_bulb_temperature` |
| HDD/CDD 10 °C & 18.3 °C | `heating_degree_days` / `cooling_degree_days` |
| Average / Max / Min / Std Precipitation | `liquid_precipitation_depth` (mean/maximum/minimum/standard_deviation) |
| Monthly Design DB (0.4/2/5/10) | `dry_bulb_temperature.monthly.percent_exceedance` |
| Monthly Design WB (0.4/2/5/10) | `wet_bulb_temperature.monthly.percent_exceedance` |
| Hottest/Coldest Month | `hottest_month` / `coldest_month` (convenience indices) |
| Hottest Month DB Range | = `daily_dry_bulb_temperature_range` at the hottest month |
| Mean Daily DB Range | `daily_dry_bulb_temperature_range` |
| Mean Daily DB/WB Range @ 5% design DB/WB | `daily_{dry,wet}_bulb_temperature_range_at_design_{dry,wet}_bulb_temperature` |
| Clear-Sky Optical Depth beam/diffuse (taub/taud) | `clear_sky_beam_optical_depth` / `clear_sky_diffuse_optical_depth` |
| All-Sky Avg/Std Monthly Global Horizontal Radiation | `daily_all_sky_solar_irradiation` (mean + standard_deviation) |

---

## 4. Deliberate exclusions (vs the ASHRAE table)

The model is **not** a 1:1 re-encoding of the ASHRAE table. Two principles drive
exclusion:

1. **Derivable quantities** are kept out of the base model where the cost of including
   them outweighs the convenience — providers can pre-compute them into an
   "ASHRAE-flavour" extension. (See the open question in §6.)
2. **Obsolete quantities** whose use cases no longer exist are dropped.

| Excluded | Cols | Reason |
|---|---|---|
| Clear-Sky Noon Beam Normal Irradiance (21st) | SP–TA | Derivable from `taub` via the HOF Ch. 14 clear-sky model. |
| Clear-Sky Noon Diffuse Horizontal Irradiance (21st) | TB–TM | Derivable from `taud`. |
| n-Year Return Period Extreme **DB** | BS–BZ | Derivable from the extreme-annual mean/std (Gumbel/empirical mixture, HOF Ch. 14). |
| n-Year Return Period Extreme **WB** | CE–CL | Same as above. |
| Humidity ratio (HR) — humidification **and** dehumidification | T, W, AW, AZ, BC | Derivable from dew point + station pressure. |
| Wind Shelter Factor (WSF) | AE | Obsolete (ASHRAE 62.2-specific). |
| Historical Trends (Station/Regional Trends, Variability, Neighbors) | UL–VP | Committee decided trends are out of scope for the base model. |
| Standard station pressure (StdP) | J | Derived from `elevation` (HOF Ch. 1). |
| ASHRAE TZ Code | L | The IANA time-zone code is stored instead. |

> An earlier short note enumerated only a subset of these exclusions; that note has
> been folded into this table and removed.
> The return-period **DB** exclusion, full **HR** exclusion, and the obsolete/derived
> station-info items were confirmed during this update (2026-06-12). Return periods are
> excluded in both flavours (DB and WB) for symmetry; if a provider needs them they
> should be added in a derived extension with the calculation documented.

### Included despite being derivable

By explicit decision, the following derivable quantities **are** carried in the base
model (they round-trip the ASHRAE table without a separate extension):

- **Enthalpy** + coincident MCDB.
- **Hottest/Coldest month** indices and the **mean daily temperature ranges**
  (including the four coincident-with-5%-design ranges).
- **Max/Min precipitation** (via `Statistics.maximum` / `minimum`).

---

## 5. What was added in this revision

**Schema (`ClimateInformation.schema.yaml`)**

- `Location.wmo_region` (Integer 1–6).
- `Statistics.maximum`, `Statistics.minimum`.
- `ClimateSummaryData`: `wet_bulb_temperature`, `wind_speed`, `enthalpy`,
  `dew_point_temperature_coincident_mean_dry_bulb_temperature`,
  `wet_bulb_temperature_coincident_mean_dry_bulb_temperature`,
  `dry_bulb_temperature_coincident_prevailing_wind_direction`,
  `enthalpy_coincident_mean_dry_bulb_temperature`,
  `wind_speed_coincident_mean_dry_bulb_temperature`,
  `clear_sky_beam_optical_depth`, `clear_sky_diffuse_optical_depth`,
  `daily_all_sky_solar_irradiation`, the five `daily_*_temperature_range*` variables,
  and the `coldest_month` / `hottest_month` indices.

Nothing was removed: variables already present in the YAML/JSON but absent from the
ASHRAE table (e.g. the air-quality and illuminance time-series variables) were left in
place.

**Examples**

- `examples/USA_IL_Chicago-v2.1-draft.json` — regenerated as valid JSON from the real
  HOF 2025 row for Chicago O'Hare (WMO 72530), with all variables above.
- `examples/GBR_Scotland_Glasgow-Bishopton-v2.1-draft.json` — new, from the HOF 2025
  row for Glasgow Bishopton (WMO 03134).

---

## 6. Open questions / known discrepancies

These are not blockers for the examples but should be resolved before the schema is
finalised:

1. **Monthly representation mismatch (YAML vs JSON).** The YAML defines
   `SummaryData.monthly` as `Array(Group(Statistics))` (an array of 12 objects). The
   JSON examples use the more compact **object-of-arrays** form
   (`monthly: { "mean": [12], "standard_deviation": [12], … }`), which is what the
   original `dry_bulb_temperature` example used. Pick one and align the other. The
   examples here follow the established object-of-arrays convention.
2. **Coincident-variable shape.** The earlier draft represented some coincident
   variables as a flat array of `{percent_time_exceeded, annual, monthly}` and others
   via the `percent_exceedance` grid. The examples here standardise on the
   `percent_exceedance` grid/lookup form for all of them. The YAML's
   `PercentTimeExceedanceCoincident` group should be reconciled with this.
3. **`SummaryDataSet.climate_data_type`.** The JSON sets `climate_data_type`
   (MEASURED/MODELED) at the data-set level, but the YAML `SummaryDataSet` group does
   not define that field. Either add it to the group or drop it from the examples.
4. **`metadata` block has no schema group.** `ClimateInformation.metadata` is typed
   `Group(Metadata)`, but no `Metadata` group is defined. Define it (data_model,
   schema, schema_version, id, description, data_timestamp, data_version, data_source,
   copyright_*, licensee, license).
5. **`DegreeDay` vs `DegreeDays`.** `ClimateSummaryData` references
   `Array(Group(DegreeDays))` but the defined group is `DegreeDay` (singular). Align
   the names.
6. **Wind direction units.** The model stores direction in radians for consistency with
   the `wind_direction` time-series variable. Confirm this is acceptable for the
   prevailing-direction summary, or switch to degrees.
7. **Month indices break the group pattern.** `coldest_month` / `hottest_month` are
   plain integers inside `ClimateSummaryData`, whose other members are all
   `Group(SummaryData)`. Acceptable as a pragmatic exception, but worth a second look.

---

## 7. Application & publication rules

Carried over from the committee notes, plus a few implied by the structure:

- **Climate zones** listed for a location apply to *that location only* — not to a
  "nearby" site.
- **Monthly arrays are ordered** January → December (index 0 = January).
- Providers are **encouraged to document each statistic's calculation** in schema/notes
  fields and to reference the original source.
- **`source_data_period` coverage** — open question: should a rule enforce that a
  declared source period covers the full time span of the values it backs (especially
  for time series)?
- **Null vs omitted** — open question: when, if ever, should a missing value be an
  explicit `null` rather than an omitted key? (See `nan_handling_python.py`.)
- **Design days, not daily values** — the committee chose not to support 365 daily
  values; "design day" constructs are preferred.
