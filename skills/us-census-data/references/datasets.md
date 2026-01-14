# Census Datasets Reference

Complete documentation for Census Bureau API datasets.

## Dataset Selection Guide

| Your Need | Dataset | Geographic Detail | Years Available |
|-----------|---------|-------------------|-----------------|
| Most reliable small-area data | ACS 5-Year | Block group+ | 2009-2023 |
| Recent data, large areas | ACS 1-Year | 65k+ population | 2005-2024 |
| Exact population counts | Decennial Census | Block | 2000, 2010, 2020 |
| Annual population between censuses | Population Estimates | County+ | 2010-2023 |

## American Community Survey (ACS) 5-Year

**Most commonly used dataset.** Combines 5 years of data for reliable estimates at small geographies.

### Endpoint
```
https://api.census.gov/data/{year}/acs/acs5
```

### Product Variants

| Variant | Endpoint | Content |
|---------|----------|---------|
| Detailed Tables | `/acs/acs5` | Full detail, all variables |
| Subject Tables | `/acs/acs5/subject` | Pre-calculated percentages |
| Data Profiles | `/acs/acs5/profile` | Summary statistics |
| Comparison Profiles | `/acs/acs5/cprofile` | Current vs prior 5-year |

### Available Years
2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023

### Geographic Coverage
- Nation, Region, Division
- State, County, County Subdivision
- Place, Census Tract, Block Group
- ZCTA (Zip Code Tabulation Area)
- Congressional District, School District
- Metropolitan/Micropolitan Statistical Area

### When to Use
- Small area analysis (tracts, block groups)
- Rural areas with small populations
- When reliability is more important than recency
- Most demographic/economic research

## American Community Survey (ACS) 1-Year

**More recent data, but limited to larger geographies.**

### Endpoint
```
https://api.census.gov/data/{year}/acs/acs1
```

### Product Variants
Same as 5-year: detailed tables, subject, profile, comparison profile.

### Available Years
2005-2019, 2021-2024 (2020 data not released due to COVID collection issues)

### Geographic Coverage
**Only areas with 65,000+ population:**
- Nation, Region, Division
- State
- County (large counties only)
- Place (large cities only)
- Metropolitan/Micropolitan Statistical Area
- Congressional District

### When to Use
- Need most recent year's data
- Analyzing large metros, states, or nation
- Tracking year-over-year changes
- Urban-focused research

## Decennial Census

**100% count of the population every 10 years.**

### 2020 Census Products

| Product | Endpoint | Content |
|---------|----------|---------|
| Redistricting (PL 94-171) | `/data/2020/dec/pl` | Race, Hispanic origin, voting age |
| Demographic and Housing | `/data/2020/dec/dhc` | Age, sex, race, households, housing |
| Demographic Profile | `/data/2020/dec/dp` | Summary demographic percentages |
| DHC-A (Detailed race) | `/data/2020/dec/dhca` | Detailed race/ethnicity groups |

### 2010 Census Products

| Product | Endpoint | Content |
|---------|----------|---------|
| Summary File 1 | `/data/2010/dec/sf1` | Race, age, sex, households |
| Summary File 2 | `/data/2010/dec/sf2` | Population by detailed race/ethnicity |

### 2000 Census Products

| Product | Endpoint | Content |
|---------|----------|---------|
| Summary File 1 | `/data/2000/dec/sf1` | Basic demographics |
| Summary File 3 | `/data/2000/dec/sf3` | Long-form sample data (income, etc.) |

### Geographic Coverage
All levels including blocks (smallest geography).

### When to Use
- Need exact counts (not estimates)
- Block-level analysis
- Redistricting/political analysis
- Historical comparisons (1990-2020)

## Population Estimates Program (PEP)

**Annual population estimates between decennial censuses.**

### Endpoint
```
https://api.census.gov/data/{year}/pep/population
```

### Available Products

| Product | Endpoint | Content |
|---------|----------|---------|
| Population | `/pep/population` | Total population, components of change |
| Characteristics | `/pep/charagegroups` | Population by age, sex, race |

### Available Years
2010-2023 (API coverage varies by product)

**Note:** Post-2021 data may require flat file downloads from Census FTP.

### Geographic Coverage
- Nation, Region, Division
- State, County
- Metropolitan Statistical Area

### When to Use
- Annual population tracking
- Components of change (births, deaths, migration)
- Population projections baseline
- Inter-censal years

## Variable Naming Conventions

### ACS Variables
```
B19013_001E
│ │     │ │
│ │     │ └─ E = Estimate, M = Margin of Error
│ │     └─── Variable number within table
│ └───────── Table number
└─────────── Table type (B = Base, C = Collapsed, S = Subject, DP = Profile)
```

### Common Table Prefixes

| Prefix | Content |
|--------|---------|
| B01 | Sex and Age |
| B02 | Race |
| B03 | Hispanic/Latino Origin |
| B05 | Citizenship Status |
| B07 | Geographic Mobility |
| B08 | Commuting |
| B11 | Household Type |
| B15 | Educational Attainment |
| B17 | Poverty Status |
| B19 | Income |
| B23 | Employment Status |
| B25 | Housing Characteristics |
| B27 | Health Insurance |

### Race Iterations
Many tables have race-specific versions:
- `B19013` - Median income (all races)
- `B19013A` - White alone
- `B19013B` - Black alone
- `B19013C` - American Indian/Alaska Native
- `B19013D` - Asian
- `B19013E` - Native Hawaiian/Pacific Islander
- `B19013F` - Other race
- `B19013G` - Two or more races
- `B19013H` - White alone, not Hispanic
- `B19013I` - Hispanic/Latino

## Margin of Error (MOE) Handling

### Understanding MOE
- ACS data are **estimates** from a sample survey
- MOE represents 90% confidence interval
- True value is likely within estimate ± MOE

### Reliability Guidelines

| Coefficient of Variation | Reliability |
|--------------------------|-------------|
| CV < 12% | High reliability |
| 12% ≤ CV < 40% | Medium reliability |
| CV ≥ 40% | Low reliability, use with caution |

**CV = (MOE / 1.645) / Estimate × 100**

### Aggregating MOE
When summing estimates:
```
MOE_sum = sqrt(MOE_1² + MOE_2² + ... + MOE_n²)
```

When calculating derived estimates (ratios, percentages), use Census Bureau formulas.

### Best Practices
1. Always report MOE with ACS estimates
2. Use 5-year estimates for small geographies
3. Avoid publishing estimates with CV > 40%
4. Consider combining geographies to improve reliability

## API Rate Limits

| Access Type | Rate Limit |
|-------------|------------|
| Without API key | ~500 requests/day (unverified) |
| With API key | No published limit |

**Recommendation:** Always use an API key for production applications.

## Data Update Schedule

| Dataset | Release Schedule |
|---------|------------------|
| ACS 1-Year | September (preliminary), December (final) |
| ACS 5-Year | December annually |
| Decennial Census | Varies by product (2020 released 2021-2023) |
| Population Estimates | December annually |

## Vintage vs Reference Year

- **Vintage**: Year the data was released
- **Reference year**: Year the data describes

For ACS 5-year:
- 2018-2022 ACS 5-Year (vintage 2022) covers reference years 2018-2022
- Endpoint uses vintage year: `/data/2022/acs/acs5`
