# Courts & Legal Datasets

Cook County criminal justice data from the State's Attorney's Office, Public Defender, and Courts.

## State's Attorney Datasets

### Sentencing
| Field | Value |
|-------|-------|
| **Dataset** | [Sentencing](https://datacatalog.cookcountyil.gov/d/tg8v-tm6u) |
| **ID** | `tg8v-tm6u` |
| **Update** | Periodic |
| **Coverage** | Felony cases |

**Key Columns:**
| Column | Type | Description |
|--------|------|-------------|
| `case_id` | number | Unique case identifier |
| `case_participant_id` | number | Unique defendant identifier |
| `received_date` | calendar_date | Date case received by Felony Review |
| `offense_category` | text | Broad offense category |
| `primary_charge` | checkbox | Whether this is the most severe charge |
| `disposition_charged_offense_title` | text | Specific offense title at disposition |
| `disposition_date` | calendar_date | Date charge was disposed |
| `sentence_type` | text | Type of sentence |
| `sentence_court` | text | Court imposing sentence |
| `sentence_judge` | text | Sentencing judge |
| `commitment_term` | number | Length of commitment |
| `commitment_unit` | text | Unit of commitment (Years, Months, Days) |

**Notes:**
- Reflects judgments imposed on guilty verdicts
- Data is by count (individual charge), not by case
- Primary charge indicates most severe charge per defendant

---

### Disposition Outcomes
| Field | Value |
|-------|-------|
| **Dataset** | [State's Attorney Felony Cases - Disposition Outcomes](https://datacatalog.cookcountyil.gov/d/anx6-yr7c) |
| **ID** | `anx6-yr7c` |
| **Update** | Periodic |
| **Coverage** | Felony case dispositions |

**Key Columns:**
| Column | Type | Description |
|--------|------|-------------|
| `case_id` | number | Case identifier |
| `case_participant_id` | number | Defendant identifier |
| `offense_category` | text | Offense category |
| `disposition_date` | calendar_date | Disposition date |
| `disposition_outcome` | text | Outcome (Guilty, Not Guilty, etc.) |
| `disposition_type` | text | How disposed (Trial, Plea, etc.) |

**Notes:**
- Culmination of fact-finding process
- Includes guilty pleas, verdicts, and dismissals

---

### Disposition Outcomes by Offense Type
| Field | Value |
|-------|-------|
| **Dataset** | [State's Attorney Felony Cases - Disposition Outcomes By Offense Type](https://datacatalog.cookcountyil.gov/d/cse8-ib7b) |
| **ID** | `cse8-ib7b` |
| **Update** | Periodic |

**Notes:**
- Aggregated view of dispositions by offense category
- Useful for high-level analysis

---

### Sentences By Offense Type
| Field | Value |
|-------|-------|
| **Dataset** | [State's Attorney Felony Cases - Sentences By Offense Type](https://datacatalog.cookcountyil.gov/d/e3fw-bkbw) |
| **ID** | `e3fw-bkbw` |
| **Update** | Periodic |

**Notes:**
- Aggregated sentencing data by offense
- Counts by individual charge, not case

---

### Initiation Results Datasets

These datasets cover arrests received by the State's Attorney's Office:

| Dataset | ID | Breakdown |
|---------|-----|-----------|
| [By Defendant Age](https://datacatalog.cookcountyil.gov/d/gs3j-9swg) | `gs3j-9swg` | Age groups |
| [By Defendant Gender](https://datacatalog.cookcountyil.gov/d/jygh-f4sn) | `jygh-f4sn` | Gender |
| [By Location Type](https://datacatalog.cookcountyil.gov/d/csm4-6i6i) | `csm4-6i6i` | City/suburb |

---

### Sentences by Location Type
| Field | Value |
|-------|-------|
| **Dataset** | [State's Attorney Felony Cases - Sentences By Offense Type and Location Type](https://datacatalog.cookcountyil.gov/d/uf6g-sr2x) |
| **ID** | `uf6g-sr2x` |
| **Update** | Periodic |

**Notes:**
- Cross-tabulation of sentences by offense and location
- Helps identify geographic patterns

---

## Common Query Patterns

### Get recent sentencing data
```
$where=disposition_date >= '2024-01-01'
$order=disposition_date DESC
$limit=1000
```

### Filter by offense category
```
$where=offense_category = 'Narcotics'
$select=case_id, disposition_date, sentence_type, commitment_term, commitment_unit
```

### Aggregate sentences by offense
```
$select=offense_category, count(*) as count, avg(commitment_term) as avg_term
$where=sentence_type = 'Prison' AND commitment_unit = 'Years'
$group=offense_category
$order=count DESC
```

### Primary charges only
```
$where=primary_charge = true
```

### Filter by sentence type
```
$where=sentence_type IN ('Prison', 'Probation', 'Jail')
```

## Offense Categories

Common offense categories in the data:
- Narcotics
- Theft
- Battery
- Robbery
- Burglary
- Homicide
- Weapons Violation
- Sex Crimes
- DUI
- Fraud
- Arson

## Disposition Outcomes

Possible disposition outcomes:
- **Guilty** - Convicted by plea or trial
- **Not Guilty** - Acquitted
- **Nolle Prosequi** - Charges dropped by prosecutor
- **Stricken Off Call (SOC)** - Case removed from docket
- **Finding of No Probable Cause** - Insufficient evidence
- **FNPC** - Finding of No Probable Cause (abbreviated)

## Sentence Types

Common sentence types:
- **Prison** - State prison commitment
- **Probation** - Supervised release
- **Jail** - County jail time
- **Conditional Discharge** - Release with conditions
- **Supervision** - Court supervision (often for first offenses)
- **Time Served** - Credit for time already spent in custody

## Important Notes

1. **Data Lag**: Criminal justice data may be delayed due to case processing
2. **Privacy**: Some data may be redacted for privacy protection
3. **Interpretation**: Consult SAO documentation for proper interpretation
4. **Changes**: Data structure may change; always verify column names
