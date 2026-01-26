# GridStatus Datasets by ISO

Complete catalog of datasets available through the GridStatus API, organized by ISO/source. Total: 454 datasets.

## Dataset Categories

Each ISO provides similar types of data:
- **Load**: System load (demand) in MW
- **LMP/SPP**: Locational Marginal Prices or Settlement Point Prices ($/MWh)
- **Fuel Mix**: Generation by fuel type (MW)
- **Forecasts**: Load, solar, wind forecasts
- **Ancillary Services**: Reserve prices, capacity
- **Constraints**: Binding transmission constraints
- **Standardized**: Pre-processed hourly/5-min data for cross-ISO comparison

## ERCOT (Texas) - 102 datasets

Electric Reliability Council of Texas. Uses "SPP" (Settlement Point Prices) instead of LMP.

### Core Datasets
| Dataset ID | Description | Frequency |
|------------|-------------|-----------|
| `ercot_load` | System-wide load | 5 min |
| `ercot_load_15_min` | System-wide load | 15 min |
| `ercot_spp_real_time_15_min` | Real-time settlement point prices | 15 min |
| `ercot_spp_day_ahead_hourly` | Day-ahead settlement point prices | Hourly |
| `ercot_fuel_mix` | Generation by fuel type | 5 min |
| `ercot_load_forecast` | Load forecast | Varies |

### Load Datasets
| Dataset ID | Description |
|------------|-------------|
| `ercot_load` | System-wide load (5 min) |
| `ercot_load_15_min` | System-wide load (15 min) |
| `ercot_load_by_forecast_zone` | Load by forecast zone |
| `ercot_load_by_weather_zone` | Load by weather zone |
| `ercot_net_load` | Load minus wind/solar |
| `ercot_load_hourly_post_settlements` | Settled hourly load |

### Price Datasets
| Dataset ID | Description | Key Columns |
|------------|-------------|-------------|
| `ercot_spp_real_time_15_min` | RT settlement prices | `location`, `spp` |
| `ercot_spp_day_ahead_hourly` | DA settlement prices | `location`, `spp` |
| `ercot_spp_dart_15_min` | DA-RT price difference | `location`, `spp` |
| `ercot_lmp_by_bus` | LMP by electrical bus | `location`, `lmp` |
| `ercot_lmp_by_bus_dam` | DA LMP by bus | `location`, `lmp` |
| `ercot_lmp_by_settlement_point` | LMP by settlement point | `location`, `lmp` |

### Location Types (ERCOT)
- **Hub**: `HB_HOUSTON`, `HB_NORTH`, `HB_SOUTH`, `HB_WEST`, `HB_BUSAVG`
- **Load Zone**: `LZ_HOUSTON`, `LZ_NORTH`, `LZ_SOUTH`, `LZ_WEST`
- **Resource Node**: Individual generation nodes

### Forecasts
| Dataset ID | Description |
|------------|-------------|
| `ercot_load_forecast` | System load forecast |
| `ercot_load_forecast_dam` | Day-ahead load forecast |
| `ercot_net_load_forecast` | Net load (load - renewables) |
| `ercot_solar_actual_and_forecast_hourly` | Solar forecast |
| `ercot_wind_actual_and_forecast_hourly` | Wind forecast |

### Ancillary Services
| Dataset ID | Description |
|------------|-------------|
| `ercot_as_prices` | Ancillary service prices |
| `ercot_as_reports` | AS market reports |
| `ercot_as_plan` | AS procurement plan |
| `ercot_mcpc_real_time_15_min` | Market clearing price for capacity |
| `ercot_real_time_as_monitor` | Real-time AS monitoring |

### Standardized (for cross-ISO comparison)
| Dataset ID | Description |
|------------|-------------|
| `ercot_standardized_5_min` | Standardized 5-min data |
| `ercot_standardized_hourly` | Standardized hourly data |

---

## CAISO (California) - 53 datasets

California Independent System Operator. Uses traditional LMP pricing.

### Core Datasets
| Dataset ID | Description | Frequency |
|------------|-------------|-----------|
| `caiso_load` | System load | 5 min |
| `caiso_lmp_real_time_5_min` | Real-time LMP | 5 min |
| `caiso_lmp_day_ahead_hourly` | Day-ahead LMP | Hourly |
| `caiso_fuel_mix` | Generation by fuel type | 5 min |
| `caiso_load_forecast` | Load forecast | Varies |

### Load Datasets
| Dataset ID | Description |
|------------|-------------|
| `caiso_load` | System load (5 min) |
| `caiso_load_hourly` | System load (hourly) |
| `caiso_load_forecast` | Short-term forecast |
| `caiso_load_forecast_dam` | Day-ahead forecast |
| `caiso_load_forecast_7_day` | 7-day forecast |

### Price Datasets
| Dataset ID | Description | Frequency |
|------------|-------------|-----------|
| `caiso_lmp_real_time_5_min` | Real-time LMP | 5 min |
| `caiso_lmp_real_time_15_min` | Real-time LMP | 15 min |
| `caiso_lmp_day_ahead_hourly` | Day-ahead LMP | Hourly |
| `caiso_lmp_dart_5_min` | DA-RT difference | 5 min |
| `caiso_lmp_hasp_15_min` | HASP LMP | 15 min |

### Location Types (CAISO)
- **Trading Hub**: `TH_NP15`, `TH_SP15`, `TH_ZP26`
- **Scheduling Point**: Interface points with other ISOs
- **Node**: Individual pricing nodes

### Forecasts & Renewables
| Dataset ID | Description |
|------------|-------------|
| `caiso_renewables_forecast_dam` | Day-ahead renewable forecast |
| `caiso_solar_and_wind_forecast_dam` | Solar/wind DA forecast |
| `caiso_renewables_hourly` | Actual renewable generation |
| `caiso_curtailment` | Renewable curtailment |

---

## PJM (Mid-Atlantic/Midwest) - 70 datasets

Pennsylvania-Jersey-Maryland Interconnection. Largest US electricity market.

### Core Datasets
| Dataset ID | Description | Frequency |
|------------|-------------|-----------|
| `pjm_load` | System load | 5 min |
| `pjm_lmp_real_time_5_min` | Real-time LMP | 5 min |
| `pjm_lmp_day_ahead_hourly` | Day-ahead LMP | Hourly |
| `pjm_fuel_mix` | Generation by fuel type | 5 min |
| `pjm_load_forecast` | Load forecast | Varies |

### Price Datasets
| Dataset ID | Description |
|------------|-------------|
| `pjm_lmp_real_time_5_min` | Real-time LMP (preliminary) |
| `pjm_lmp_real_time_hourly` | Real-time LMP (hourly) |
| `pjm_lmp_day_ahead_hourly` | Day-ahead LMP |
| `pjm_lmp_dart_5_min` | DA-RT difference |
| `pjm_settlements_verified_lmp_5_min` | Verified settlement LMP |

### Location Types (PJM)
- **Zone**: `AECO`, `AEP`, `APS`, `ATSI`, `BGE`, `COMED`, `DAY`, `DEOK`, `DOM`, `DPL`, `DUQ`, `EKPC`, `JCPL`, `METED`, `PECO`, `PENELEC`, `PEPCO`, `PPL`, `PSEG`, `RECO`
- **Hub**: `WESTERN HUB`, `EASTERN HUB`, `AEP-DAYTON HUB`, `NI-HUB`
- **Aggregate**: Regional aggregations
- **Interface**: External interface points

### Ancillary Services
| Dataset ID | Description |
|------------|-------------|
| `pjm_as_market_results_dam` | DA ancillary service results |
| `pjm_as_market_results_real_time` | RT ancillary service results |
| `pjm_regulation_prices_5_min` | Regulation prices |
| `pjm_operational_reserves` | Operating reserve data |

---

## MISO (Midwest) - 42 datasets

Midcontinent Independent System Operator.

### Core Datasets
| Dataset ID | Description | Frequency |
|------------|-------------|-----------|
| `miso_load` | System load | 5 min |
| `miso_lmp_real_time_5_min` | Real-time LMP | 5 min |
| `miso_lmp_day_ahead_hourly` | Day-ahead LMP | Hourly |
| `miso_fuel_mix` | Generation by fuel type | 5 min |

### Price Datasets
| Dataset ID | Description |
|------------|-------------|
| `miso_lmp_real_time_5_min` | RT LMP (preliminary) |
| `miso_lmp_real_time_5_min_ex_post_final` | RT LMP (final) |
| `miso_lmp_day_ahead_hourly` | DA LMP |
| `miso_lmp_day_ahead_hourly_ex_ante` | DA LMP ex-ante |
| `miso_lmp_dart_ex_post_5_min` | DA-RT difference |

### Location Types (MISO)
- **Hub**: `INDIANA.HUB`, `ILLINOIS.HUB`, `MICHIGAN.HUB`, `MINN.HUB`, `ARKANSAS.HUB`, `LOUISIANA.HUB`, `MS.HUB`, `TEXAS.HUB`
- **Zone**: Load zones
- **Node**: Individual pricing nodes

---

## NYISO (New York) - 27 datasets

New York Independent System Operator.

### Core Datasets
| Dataset ID | Description | Frequency |
|------------|-------------|-----------|
| `nyiso_load` | System load | 5 min |
| `nyiso_lmp_real_time_5_min` | Real-time LMP | 5 min |
| `nyiso_lmp_day_ahead_hourly` | Day-ahead LMP | Hourly |
| `nyiso_fuel_mix` | Generation by fuel type | 5 min |

### Location Types (NYISO)
- **Zone**: A through K (WEST, GENESE, CENTRL, NORTH, MHK VL, CAPITL, HUD VL, MILLWD, DUNWOD, N.Y.C., LONGIL)
- **Generator**: Individual generation nodes

---

## ISO-NE (New England) - 43 datasets

ISO New England.

### Core Datasets
| Dataset ID | Description | Frequency |
|------------|-------------|-----------|
| `isone_load` | System load | 5 min |
| `isone_lmp_real_time_5_min` | Real-time LMP | 5 min |
| `isone_lmp_day_ahead_hourly` | Day-ahead LMP | Hourly |
| `isone_fuel_mix` | Generation by fuel type | 5 min |

### Location Types (ISO-NE)
- **Zone**: `.Z.MAINE`, `.Z.NEWHAMPSHIRE`, `.Z.VERMONT`, `.Z.CONNECTICUT`, `.Z.RHODEISLAND`, `.Z.SEMASS`, `.Z.WCMASS`, `.Z.NEMA`
- **Hub**: `.H.INTERNAL_HUB`
- **Node**: Individual nodes

---

## SPP (Southwest/Central) - 29 datasets

Southwest Power Pool.

### Core Datasets
| Dataset ID | Description | Frequency |
|------------|-------------|-----------|
| `spp_load` | System load | 5 min |
| `spp_lmp_real_time_5_min` | Real-time LMP | 5 min |
| `spp_lmp_day_ahead_hourly` | Day-ahead LMP | Hourly |
| `spp_fuel_mix` | Generation by fuel type | 5 min |

---

## IESO (Ontario, Canada) - 53 datasets

Independent Electricity System Operator (Ontario).

### Core Datasets
| Dataset ID | Description | Frequency |
|------------|-------------|-----------|
| `ieso_load` | System load | 5 min |
| `ieso_lmp_real_time_5_min` | Real-time LMP | 5 min |
| `ieso_lmp_day_ahead_hourly` | Day-ahead LMP | Hourly |
| `ieso_fuel_mix` | Generation by fuel type | 5 min |
| `ieso_hoep_real_time_hourly` | Hourly Ontario Energy Price | Hourly |

---

## AESO (Alberta, Canada) - 21 datasets

Alberta Electric System Operator.

### Core Datasets
| Dataset ID | Description |
|------------|-------------|
| `aeso_load` | System load |
| `aeso_pool_price` | Pool price |
| `aeso_fuel_mix` | Generation by fuel type |

---

## EIA (US Energy Information Administration) - 10 datasets

National-level data from EIA.

| Dataset ID | Description |
|------------|-------------|
| `eia_regional_hourly` | Regional hourly data |
| `eia_fuel_mix_hourly` | Fuel mix by region |
| `eia_ba_interchange_hourly` | Balancing authority interchange |
| `eia_henry_hub_natural_gas_spot_prices_daily` | Natural gas prices |

---

## Cross-ISO Datasets

| Dataset ID | Description |
|------------|-------------|
| `isos_latest` | Latest data for all ISOs |
| `all_records` | Record values across ISOs |
| `all_records_timeseries` | Record values over time |

---

## Dataset Naming Convention

```
{iso}_{data_type}_{market}_{frequency}
```

Examples:
- `ercot_spp_real_time_15_min` - ERCOT settlement prices, real-time, 15-minute
- `caiso_lmp_day_ahead_hourly` - CAISO LMP, day-ahead, hourly
- `pjm_lmp_dart_5_min` - PJM day-ahead vs real-time difference, 5-minute

### Market Types
- `real_time` / `rt` - Real-time market
- `day_ahead` / `dam` - Day-ahead market
- `dart` - Day-ahead minus real-time (spread)
- `hasp` - Hour-ahead scheduling process (CAISO)

### Frequency Suffixes
- `5_min` - 5-minute intervals
- `15_min` - 15-minute intervals
- `hourly` - Hourly intervals
- `daily` - Daily values
