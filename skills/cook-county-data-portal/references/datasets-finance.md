# Finance & Administration Datasets

Cook County budget, payroll, procurement, and transparency data.

## Payroll Datasets

### Employee Payroll (Current)
| Field | Value |
|-------|-------|
| **Dataset** | [Employee Payroll](https://datacatalog.cookcountyil.gov/d/xu6t-uvny) |
| **ID** | `xu6t-uvny` |
| **Update** | Quarterly |
| **Coverage** | FY2016 to present |

**Key Columns:**
| Column | Type | Description |
|--------|------|-------------|
| `fiscal_year` | number | County fiscal year |
| `fiscal_quarter` | number | Quarter (1-4) |
| `fiscal_period` | text | Year + Quarter combined |
| `first_name` | text | Employee first name |
| `last_name` | text | Employee last name |
| `bureau` | text | Bureau name |
| `office` | text | Office ID |
| `office_name` | text | Office name |
| `job_code` | text | Job classification code |
| `job_title` | text | Job title |
| `original_hire_date` | calendar_date | Date of hire |
| `base_pay` | number | Base salary for the quarter |
| `employee_identifier` | text | Unique employee ID (consistent across time) |

**Notes:**
- Excludes Forest Preserves employees
- Fiscal quarters: Q1 (Dec-Feb), Q2 (Mar-May), Q3 (Jun-Aug), Q4 (Sep-Nov)
- Pay periods spanning quarters assigned to quarter of pay period end date
- Employee Identifier allows tracking across name changes

---

### Historical Payroll Datasets

For data prior to FY2016:

| Dataset | ID | Period |
|---------|-----|--------|
| [FY2017 Q3](https://datacatalog.cookcountyil.gov/d/tvzv-dhts) | `tvzv-dhts` | Jun-Aug 2017 |
| [FY2017 Q2](https://datacatalog.cookcountyil.gov/d/s36d-k9ar) | `s36d-k9ar` | Mar-May 2017 |
| [FY2016](https://datacatalog.cookcountyil.gov/d/iviu-4wng) | `iviu-4wng` | FY2016 |
| [2015 Salaries](https://datacatalog.cookcountyil.gov/d/9tzu-m4zi) | `9tzu-m4zi` | Nov 2015 |
| [2014 Salaries](https://datacatalog.cookcountyil.gov/d/hdna-35se) | `hdna-35se` | Aug 2014 |
| [2013 Salaries](https://datacatalog.cookcountyil.gov/d/fxa5-tdd8) | `fxa5-tdd8` | 2013 |
| [2011 Salaries](https://datacatalog.cookcountyil.gov/d/wb2w-sasu) | `wb2w-sasu` | Sep 2011 |

---

## Procurement Datasets

### Awarded Contracts & Amendments
| Field | Value |
|-------|-------|
| **Dataset** | [Procurement - Awarded Contracts & Amendments](https://datacatalog.cookcountyil.gov/d/qh8j-6k63) |
| **ID** | `qh8j-6k63` |
| **Update** | As awarded |
| **Coverage** | FY2015 to present (amendments) |

**Key Columns:**
| Column | Type | Description |
|--------|------|-------------|
| `contract_number` | text | Contract number |
| `vendor_number` | number | Vendor ID |
| `vendor_name` | text | Vendor name |
| `amount` | number | Contract/amendment amount |
| `description` | text | Contract description |
| `system_release` | calendar_date | Date released from Procurement |
| `lead_department` | text | Lead department |
| `start_date` | calendar_date | Contract start date |
| `end_date` | calendar_date | Contract end date |
| `contract_pdf` | url | Link to contract PDF |

**Notes:**
- Includes new contracts and amendments
- Amendments may be extensions, renewals, increases, decreases, or scope changes
- Amount may be blank for revenue-generating contracts

---

### Bid Tabulations
| Field | Value |
|-------|-------|
| **Dataset** | [Procurement - Bid Tabulations](https://datacatalog.cookcountyil.gov/d/32au-zaqn) |
| **ID** | `32au-zaqn` |
| **Update** | After bid openings |
| **Coverage** | June 2016 to present |

**Key Columns:**
| Column | Type | Description |
|--------|------|-------------|
| `bid_number` | text | Bid solicitation number |
| `vendor_name` | text | Bidder name |
| `bid_amount` | number | Bid amount |
| `bid_date` | calendar_date | Date of bid opening |
| `description` | text | Bid description |

**Notes:**
- Preliminary data, subject to review
- Bids $25,000+ are publicly opened
- RFP/RFQ/RFI responses listed by sealed package names

---

### Intent to Award
| Field | Value |
|-------|-------|
| **Dataset** | [Procurement - Intent to Award](https://datacatalog.cookcountyil.gov/d/bgq7-v7ms) |
| **ID** | `bgq7-v7ms` |
| **Update** | Before Board meetings |

**Key Columns:**
| Column | Type | Description |
|--------|------|-------------|
| `vendor_name` | text | Recommended vendor |
| `mbe_participation` | text | Minority Business Enterprise participation |
| `wbe_participation` | text | Women Business Enterprise participation |
| `dbe_participation` | text | Disadvantaged Business Enterprise participation |

**M/W/DBE Codes:**
- 4 = Native American
- 5 = African American
- 7 = Female
- 8 = Asian
- 9 = Hispanic

---

### Intent to Execute
| Field | Value |
|-------|-------|
| **Dataset** | [Procurement - Intent to Execute](https://datacatalog.cookcountyil.gov/d/ag43-fvd7) |
| **ID** | `ag43-fvd7` |
| **Update** | As posted |

---

## Human Resources Datasets

### Exempt Positions
| Field | Value |
|-------|-------|
| **Dataset** | [Human Resources - Exempt Positions](https://datacatalog.cookcountyil.gov/d/6ybd-qcyy) |
| **ID** | `6ybd-qcyy` |
| **Update** | As updated |

**Notes:**
- Positions exempt from civil service protections
- Policy-making or confidential positions

---

### Collective Bargaining Agreements
| Field | Value |
|-------|-------|
| **Dataset** | [Human Resources - Collective Bargaining Agreements](https://datacatalog.cookcountyil.gov/d/8tar-cztq) |
| **ID** | `8tar-cztq` |
| **Update** | As ratified |

---

## Inspector General Datasets

### Quarterly Reports
| Field | Value |
|-------|-------|
| **Dataset** | [Inspector General - Quarterly Reports](https://datacatalog.cookcountyil.gov/d/fujx-q5fd) |
| **ID** | `fujx-q5fd` |
| **Update** | Quarterly |

---

### Employment Action Reports
| Field | Value |
|-------|-------|
| **Dataset** | [Inspector General - Employment Quarterly Action Reports](https://datacatalog.cookcountyil.gov/d/u6q5-2knd) |
| **ID** | `u6q5-2knd` |
| **Update** | Quarterly |

**Notes:**
- Hires, promotions, transfers, terminations
- Per Employment Plan compliance

---

## Budget Datasets

### Budget Archive
| Field | Value |
|-------|-------|
| **Dataset** | [Budget Archive](https://datacatalog.cookcountyil.gov/d/q379-w3q5) |
| **ID** | `q379-w3q5` |
| **Update** | Annually |

---

## Registered Business Datasets

These datasets list businesses registered with Cook County Department of Revenue:

| Business Type | ID |
|--------------|-----|
| [Amusement Operators](https://datacatalog.cookcountyil.gov/d/89ad-rfuq) | `89ad-rfuq` |
| [Firearm Retailers](https://datacatalog.cookcountyil.gov/d/v6c6-fyie) | `v6c6-fyie` |
| [New Motor Vehicle Dealers](https://datacatalog.cookcountyil.gov/d/ng43-255b) | `ng43-255b` |
| [Wholesale Tobacco Dealers](https://datacatalog.cookcountyil.gov/d/fqrs-pn3x) | `fqrs-pn3x` |
| [Wholesale Alcohol Dealers](https://datacatalog.cookcountyil.gov/d/ud3j-i2ws) | `ud3j-i2ws` |
| [Diesel Distributors](https://datacatalog.cookcountyil.gov/d/f2q7-6uiv) | `f2q7-6uiv` |
| [Gasoline Distributors](https://datacatalog.cookcountyil.gov/d/f25x-6dab) | `f25x-6dab` |
| [Parking/Valet Operators](https://datacatalog.cookcountyil.gov/d/muak-hbtd) | `muak-hbtd` |
| [Personal Property Dealers](https://datacatalog.cookcountyil.gov/d/h9vb-3tcy) | `h9vb-3tcy` |

**Note:** Lists updated monthly. Contact 312-603-6328 for real-time accuracy.

---

## Common Query Patterns

### Total payroll by bureau
```
$select=bureau, sum(base_pay) as total_pay
$where=fiscal_year = 2024
$group=bureau
$order=total_pay DESC
```

### Employee lookup
```
$where=upper(last_name) = 'SMITH' AND fiscal_year = 2024
$order=fiscal_quarter DESC
```

### Contracts above threshold
```
$where=amount > 1000000
$order=amount DESC
$limit=50
```

### Contracts by department
```
$select=lead_department, count(*) as contracts, sum(amount) as total_value
$group=lead_department
$order=total_value DESC
```

### Highest paid positions
```
$where=fiscal_year = 2024 AND fiscal_quarter = 4
$order=base_pay DESC
$limit=100
```

## Fiscal Year Calendar

Cook County fiscal year runs December 1 to November 30:

| Quarter | Months |
|---------|--------|
| Q1 | December - February |
| Q2 | March - May |
| Q3 | June - August |
| Q4 | September - November |

Fiscal Year 2024 = December 2023 through November 2024
