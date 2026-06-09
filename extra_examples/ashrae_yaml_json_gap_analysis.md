# ASHRAE HOF 2025 ↔ YAML ↔ JSON Gap Analysis

Comparison of the ASHRAE Handbook of Fundamentals 2025 Climate Design Conditions
spreadsheet (`HOF_2025_Climate_Design_Conditions_SI.xlsx`, single `Stations` sheet,
588 columns, header rows 1–4) against `schema/ClimateInformation.schema.yaml` and the
`examples/USA_IL_Chicago-v2.1-draft.json` example.

---

## Part 1 — ASHRAE Excel variables missing from the YAML

The YAML's `ClimateSummaryData` currently covers: `dry_bulb_temperature`,
`dew_point_temperature`, `relative_humidity`,
`dry_bulb_temperature_coincident_mean_wet_bulb_temperature` (MCWB),
`dry_bulb_temperature_coincident_mean_wind_speed` (MCWS),
`daily_average_dry_bulb_temperature` (+ its std), `liquid_precipitation_depth`
(mean + std), `heating_degree_days`, `cooling_degree_days`. `Statistics` also covers the
**Extreme Annual DB** mean/std min & max. Everything below is in the Excel but **not**
representable in the YAML.

### Station Information (cols A–O)
- `Region` (WMO region) — col A
- `StdP` (standard station pressure) — col J *(likely intentional: YAML notes it's derived from elevation)*
- `TZ Code` (ASHRAE tz code, e.g. NAC) — col L *(YAML stores IANA code instead — intentional)*

### Annual Heating & Humidification (cols P–AE)
- `Coldest Month` (index) — col P
- Humidification `HR` (humidity ratio coincident with humidification DP) — cols T, W
- Humidification `MCDB` (mean coincident DB with DP) — cols U, X → *no `dew_point_temperature_coincident_mean_dry_bulb_temperature`*
- `Coldest Month WS / MCDB` (extreme low-end wind speed at 0.4%/1% + coincident DB) — cols Y–AB
- `PCWD` (prevailing coincident wind direction to 99.6% DB) — col AD
- `Wind Shelter Factor` — col AE

### Annual Cooling, Dehumidification & Enthalpy (cols AF–BK)
- `Hottest Month` (index) — col AF
- `Hottest Month DB Range` — col AG
- `Evaporation WB` (wet-bulb design temp, 0.4/1/2%) + its `MCDB` — cols AN–AS → *no summary `wet_bulb_temperature`, no `wet_bulb_temperature_coincident_mean_dry_bulb_temperature`*
- Dehumidification `HR` and `MCDB` — cols AW, AX, AZ, BA, BC, BD
- `Enthalpy` (0.4/1/2%) and its coincident `MCDB` — cols BE–BJ → *the JSON's `enthalpy_coincident_mean_dry_bulb_temperature` has no YAML home*
- `Extreme Max WB` — col BK

### Extreme Annual Design Conditions (cols BL–CL)
- `Extreme Annual WS` (1 / 2.5 / 5%) — cols BL–BN → *no summary `wind_speed`*
- `n-Year Return Period Extreme DB` (n = 5/10/20/50, min & max) — cols BS–BZ → *`Statistics` has no return-period element*
- `Extreme Annual WB` (mean & std, min & max) — cols CA–CD
- `n-Year Return Period Extreme WB` — cols CE–CL

### Precipitation (cols FZ–HY)
- `Maximum Precipitation` (annual + monthly) — cols GM–GY
- `Minimum Precipitation` (annual + monthly) — cols GZ–HL

### Wind Speed (cols FM–FY)
- `Average Wind Speed` (annual + 12 monthly) → JSON has `wind_speed`, **not in YAML summary**

### Monthly Design Wet Bulb & Mean Coincident Dry Bulb (cols LR–PI)
- `Monthly Design Wet Bulb Temperature` (0.4 / 2 / 5 / 10%) — no summary `wet_bulb_temperature`
- `Mean DB coincident with monthly design WB` → no `wet_bulb_temperature_coincident_mean_dry_bulb_temperature`

### Mean Daily Temperature Range (cols PJ–RQ) — entire section absent
- `Mean Daily DB Temperature Range`
- `Mean Daily DB Range coincident w/ 5% design DB`
- `Mean Daily WB Range coincident w/ 5% design DB`
- `Mean Daily DB Range coincident w/ 5% design WB`
- `Mean Daily WB Range coincident w/ 5% design WB`

### Clear-Sky Solar Irradiance (cols RR–TM)
- `Clear-Sky Beam Optical Depth (taub)` → JSON `clear_sky_beam_optical_depth`, **not in YAML**
- `Clear-Sky Diffuse Optical Depth (taud)` → JSON `clear_sky_diffuse_optical_depth`, **not in YAML**
- `Clear-Sky Noon Beam Normal Irradiance (21st day)` — cols SP–TA
- `Clear-Sky Noon Diffuse Horizontal Irradiance (21st day)` — cols TB–TM

### All-Sky Solar Radiation (cols TN–UK)
- `All-Sky Avg Monthly Global Horizontal Radiation` (+ its std) → JSON has `daily_all_sky_solar_irradiation`, **not in YAML**

### Historical Trends (cols UL–VP) — entire section absent
- `Station Trends`, `Station Variability`, `Regional Trends`, `Neighbors` — each spanning DBAvg, Heating (99% DB, 99% DP), Cooling (1% DB, 1% WB, 1% DP), and Degree-Days (HDD10.0, HDD18.3, CDD10.0, CDD18.3)

> Note: the "Temperatures, Degree-Days, **and Degree-Hours**" section title (col CM) implies
> degree-hours, but there are no degree-hour columns in the file, so nothing to add there.

---

## Part 2 — JSON variables that aren't in the YAML

These keys appear in the Chicago JSON's `summary_data` but have **no matching element** in
`ClimateSummaryData`:

| JSON key | In YAML? |
|---|---|
| `dry_bulb_temperature_coincident_prevailing_wind_direction` | ✗ |
| `clear_sky_beam_optical_depth` | ✗ |
| `clear_sky_diffuse_optical_depth` | ✗ |
| `daily_all_sky_solar_irradiation` | ✗ |
| `enthalpy_coincident_mean_dry_bulb_temperature` | ✗ |
| `wind_speed` | ✗ |
| `wet_bulb_temperature` | ✗ |
| `humidity_ratio` | ✗ |
| `absolute_humidity` | ✗ (not even a TimeSeries variable) |

(`dew_point_temperature` is the reverse case — defined in the YAML but unused in the JSON,
which is fine.)

### Other JSON↔YAML mismatches worth flagging (not "missing variables," but they break alignment)

- **Field-name mismatches:**
  - `wban_station_id` (JSON) vs `wban_station_number` (YAML)
  - `percent_times_exceeded` (JSON grid_variables) vs `percent_time_exceeded` (YAML `PercentTimeExceedanceGridVariables`)
  - `end_time` (JSON source data periods) vs `ending_time` (YAML `SourceDataPeriod`)
- **Enum mismatch:** the summary set uses `"climate_data_type": "PROJECTED"`, but
  `SummaryDataSet.climate_data_type` only allows the summary enum (MEASURED / MODELED).
  `PROJECTED` belongs to `TimeSeriesClimateDataType`.
- **Undefined groups/enums the JSON relies on:** the YAML references `Group(Metadata)`,
  `Enumeration(SummaryClimateDataType)`, and `Enumeration(DataSourceType)`, but the
  actually-defined blocks are (none for Metadata), `SummaryDataSourceType`, and
  `TimeSeriesDataSourceType`. So the JSON's entire `metadata` block has no schema definition
  behind it.
- **Time-series structure mismatch:** JSON `time_series_data_sets[*]` uses a singular
  `source_data_period` object with variables inline, but the YAML `TimeSeriesDataSet` expects
  `climate_data_type`, `time_intervals` (array of `TimeInterval`), and a `time_series` group
  whose members reference TimeInterval `id`s.
- **Invalid JSON:** the file contains `//` comments (lines 395, 692) — those must be removed
  for it to parse as JSON.
