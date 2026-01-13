# Health & Medical Examiner Datasets

Cook County health and mortality data from the Medical Examiner's Office.

## Medical Examiner Datasets

### Case Archive
| Field | Value |
|-------|-------|
| **Dataset** | [Medical Examiner Case Archive](https://datacatalog.cookcountyil.gov/d/cjeq-bs86) |
| **ID** | `cjeq-bs86` |
| **Update** | Daily |
| **Coverage** | August 2014 to present |

**Key Columns:**
| Column | Type | Description |
|--------|------|-------------|
| `casenumber` | text | ME case number |
| `incident_date` | calendar_date | Date incident occurred |
| `death_date` | calendar_date | Date pronounced dead |
| `age` | number | Age of decedent |
| `gender` | text | Gender |
| `race` | text | Race |
| `latino` | checkbox | Latino ethnicity |
| `manner` | text | Manner of death (Homicide, Suicide, Natural, Accident, Undetermined) |
| `primarycause` | text | Primary cause of death (combined) |
| `secondarycause` | text | Secondary cause of death |
| `incident_city` | text | City where incident occurred |
| `incident_zip` | text | ZIP code of incident |
| `commissioner_district` | text | Cook County Commissioner District |
| `latitude` | number | Incident location latitude |
| `longitude` | number | Incident location longitude |

**Notes:**
- Not all deaths in Cook County are ME jurisdiction
- ME determines cause/manner for deaths under its jurisdiction
- COVID-19 jurisdiction changed April 2022 (hospital/nursing home deaths excluded unless other factors)

---

### COVID-19 Related Deaths
| Field | Value |
|-------|-------|
| **Dataset** | [Medical Examiner Case Archive - COVID-19 Related Deaths](https://datacatalog.cookcountyil.gov/d/3trz-enys) |
| **ID** | `3trz-enys` |
| **Update** | Daily |
| **Coverage** | March 2020 to present |

**Notes:**
- Filtered view of Case Archive where "covid" appears in cause fields
- Effective April 2022, ME no longer takes most hospital/nursing home COVID deaths
- For broader COVID data, see Illinois DPH dashboard

---

### Manner of Death Chart
| Field | Value |
|-------|-------|
| **Dataset** | [Medical Examiner Case Archive - Manner of Death Chart](https://datacatalog.cookcountyil.gov/d/jjtx-2ras) |
| **ID** | `jjtx-2ras` |
| **Update** | Daily |

**Notes:**
- Visualization-ready aggregation of manner of death
- Same underlying data as Case Archive

---

### Unidentified Persons
| Field | Value |
|-------|-------|
| **Dataset** | [Medical Examiner - Unidentified Persons](https://datacatalog.cookcountyil.gov/d/y8dh-5w5c) |
| **ID** | `y8dh-5w5c` |
| **Update** | As needed |

**Key Columns:**
| Column | Type | Description |
|--------|------|-------------|
| `me_case_number` | text | ME case number |
| `date_found` | calendar_date | Date remains found |
| `location` | text | Location found |
| `sex` | text | Estimated sex |
| `estimated_age` | text | Estimated age range |
| `race` | text | Estimated race |
| `description` | text | Physical description |

**Notes:**
- Contact Deputy Chief Investigator for matching to missing persons
- Images may be graphic
- Also listed on NAMUS.gov

---

### Unclaimed Persons
| Field | Value |
|-------|-------|
| **Dataset** | [Medical Examiner - Unclaimed Persons](https://datacatalog.cookcountyil.gov/d/jmub-3h99) |
| **ID** | `jmub-3h99` |
| **Update** | As needed |

**Notes:**
- List of unclaimed decedents
- Contact Indigent Coordinator for next of kin claims
- Unclaimed indigents cremated/buried within 60 days

---

### Indigent Cremations
| Field | Value |
|-------|-------|
| **Dataset** | [Medical Examiner Indigent Cremations](https://datacatalog.cookcountyil.gov/d/f9wk-2wb9) |
| **ID** | `f9wk-2wb9` |
| **Update** | As needed |

**Notes:**
- List of unclaimed indigents cremated by ME office

---

### Burial Locations
| Field | Value |
|-------|-------|
| **Dataset** | [Medical Examiner - Burial Locations](https://datacatalog.cookcountyil.gov/d/hc2f-evny) |
| **ID** | `hc2f-evny` |
| **Update** | As needed |

**Notes:**
- Final disposition sites of indigents buried by ME office
- Includes lat/long for Homewood Memorial Gardens
- Includes grave/lot/block for Mount Olivet

---

## Common Query Patterns

### Recent homicides
```
$where=manner = 'Homicide' AND death_date >= '2024-01-01'
$order=death_date DESC
$limit=100
```

### Deaths by manner and year
```
$select=manner, date_extract_y(death_date) as year, count(*) as count
$group=manner, date_extract_y(death_date)
$order=year DESC, count DESC
```

### Filter by age range
```
$where=age >= 18 AND age <= 35
```

### Geographic analysis
```
$where=incident_city = 'Chicago' AND manner = 'Homicide'
$select=incident_zip, count(*) as count
$group=incident_zip
$order=count DESC
```

### Opioid-related deaths
```
$where=primarycause like '%OPIOID%' OR primarycause like '%FENTANYL%' OR primarycause like '%HEROIN%'
```

### Gun violence
```
$where=manner = 'Homicide' AND primarycause like '%GUNSHOT%'
```

## Manner of Death Categories

| Manner | Description |
|--------|-------------|
| **Homicide** | Death caused by another person with intent to injure or kill |
| **Suicide** | Self-inflicted death with intent to die |
| **Accident** | Unintentional death |
| **Natural** | Death due to disease or natural causes |
| **Undetermined** | Manner cannot be determined |

## Important Notes

1. **Jurisdiction**: ME only handles deaths under its jurisdiction (unattended, violent, suspicious deaths)
2. **Privacy**: Some identifying information may be limited
3. **COVID Changes**: After April 2022, COVID deaths in healthcare settings generally excluded
4. **Cause vs Manner**: Cause is why they died; manner is how (intent/circumstances)
5. **Lag Time**: Data updates daily but may lag for pending investigations
