# Popular Chicago Datasets

Quick reference for commonly requested datasets. **Always verify column names via metadata endpoint before querying.**

## Dataset Lookup by Topic

| If user asks about... | Use this dataset |
|-----------------------|------------------|
| Crime, shootings, theft | Crimes - 2001 to Present (`ijzp-q8t2`) |
| Car accidents, traffic crashes | Traffic Crashes (`85ca-t3if`) |
| 311, service requests, complaints | 311 Service Requests (`v6vf-nfxy`) |
| Towed cars, impound | Towed Vehicles (`ygr5-vcbg`) |
| Construction, building permits | Building Permits (`ydr8-5enu`) |
| Business licenses, new businesses | Business Licenses (`r5kz-chrr`) |
| Restaurant inspections, health | Food Inspections (`4ijn-s7e5`) |
| Bike sharing, Divvy | Divvy Trips (`fg6s-gzvg`) |
| Potholes, street repairs | 311 Service Requests (filter: `sr_type LIKE '%pothole%'`) |
| Graffiti removal | 311 Service Requests (filter: `sr_type LIKE '%graffiti%'`) |
| Employee salaries | Employee Salaries (`xzkq-xp2w`) |
| Lobbyist activity | Lobbyist Data (`tq3e-t5yq`) |

---

## Public Safety

### Crimes - 2001 to Present
- **ID:** `ijzp-q8t2`
- **Link:** https://data.cityofchicago.org/d/ijzp-q8t2
- **Key columns:** `date`, `primary_type`, `description`, `arrest`, `domestic`, `beat`, `district`, `ward`, `community_area`, `latitude`, `longitude`, `location`
- **Update:** Daily (excludes most recent 7 days)
- **Notes:** Privacy-protected - addresses shown at block level only. Types include: THEFT, BATTERY, CRIMINAL DAMAGE, ASSAULT, BURGLARY, NARCOTICS, MOTOR VEHICLE THEFT, ROBBERY, etc.

### Traffic Crashes - Crashes
- **ID:** `85ca-t3if`
- **Link:** https://data.cityofchicago.org/d/85ca-t3if
- **Key columns:** `crash_date`, `crash_type`, `posted_speed_limit`, `traffic_control_device`, `weather_condition`, `lighting_condition`, `first_crash_type`, `injuries_total`, `injuries_fatal`, `latitude`, `longitude`
- **Update:** Daily
- **Related:** Vehicles (`68nd-jvt3`), People (`u6pd-qa9d`)

---

## City Services

### 311 Service Requests
- **ID:** `v6vf-nfxy`
- **Link:** https://data.cityofchicago.org/d/v6vf-nfxy
- **Key columns:** `sr_number`, `sr_type`, `sr_short_code`, `created_date`, `closed_date`, `status`, `ward`, `community_area`, `latitude`, `longitude`
- **Update:** Daily
- **Common sr_types:** "Pothole in Street", "Graffiti Removal Request", "Street Light Out", "Tree Trim Request", "Abandoned Vehicle", "Rodent Baiting/Rat Complaint"

### Towed Vehicles
- **ID:** `ygr5-vcbg`
- **Link:** https://data.cityofchicago.org/d/ygr5-vcbg
- **Key columns:** `tow_date`, `make`, `style`, `model`, `color`, `plate`, `state`, `towed_to_address`, `inventory_number`
- **Update:** Daily
- **Notes:** Rolling 90-day window only. No location of tow origin.

---

## Business & Permits

### Building Permits
- **ID:** `ydr8-5enu`
- **Link:** https://data.cityofchicago.org/d/ydr8-5enu
- **Key columns:** `id`, `permit_`, `permit_type`, `issue_date`, `work_description`, `total_fee`, `street_number`, `street_direction`, `street_name`, `suffix`, `latitude`, `longitude`
- **Update:** Daily
- **permit_type values:** "PERMIT - NEW CONSTRUCTION", "PERMIT - RENOVATION/ALTERATION", "PERMIT - ELECTRIC WIRING", etc.

### Business Licenses
- **ID:** `r5kz-chrr`
- **Link:** https://data.cityofchicago.org/d/r5kz-chrr
- **Key columns:** `license_id`, `account_number`, `legal_name`, `doing_business_as_name`, `license_description`, `business_activity`, `license_status`, `date_issued`, `expiration_date`, `ward`, `latitude`, `longitude`
- **Update:** Daily
- **Notes:** One row per license; businesses may have multiple licenses.

### Food Inspections
- **ID:** `4ijn-s7e5`
- **Link:** https://data.cityofchicago.org/d/4ijn-s7e5
- **Key columns:** `inspection_id`, `dba_name`, `aka_name`, `license_`, `facility_type`, `risk`, `inspection_date`, `inspection_type`, `results`, `violations`, `latitude`, `longitude`
- **Update:** Daily
- **results values:** "Pass", "Fail", "Pass w/ Conditions", "Out of Business", "No Entry"
- **Notes:** `violations` is a pipe-delimited text field with violation codes and comments.

---

## Transportation

### Divvy Trips
- **ID:** `fg6s-gzvg`
- **Link:** https://data.cityofchicago.org/d/fg6s-gzvg
- **Key columns:** `trip_id`, `start_time`, `end_time`, `bikeid`, `tripduration`, `from_station_id`, `from_station_name`, `to_station_id`, `to_station_name`, `usertype`
- **Update:** Monthly
- **Notes:** Excludes trips under 60 seconds and staff service trips.

### Divvy Bicycle Stations
- **ID:** `bbyy-e7gq`
- **Link:** https://data.cityofchicago.org/d/bbyy-e7gq
- **Key columns:** `id`, `station_name`, `total_docks`, `docks_in_service`, `status`, `latitude`, `longitude`
- **Update:** Near real-time

---

## Government & Finance

### Employee Salaries
- **ID:** `xzkq-xp2w`
- **Link:** https://data.cityofchicago.org/d/xzkq-xp2w
- **Key columns:** `name`, `job_titles`, `department`, `full_or_part_time`, `salary_or_hourly`, `annual_salary`, `hourly_rate`
- **Update:** Annually

---

## Metadata Quick Check

Get full schema for any dataset:
```bash
curl "https://data.cityofchicago.org/api/views/{ID}" | jq '.columns[] | {fieldName, dataTypeName, description}'
```

## Find More Datasets

Search the catalog API:
```bash
curl "https://api.us.socrata.com/api/catalog/v1?domains=data.cityofchicago.org&q=YOUR_KEYWORDS"
```

Or browse: https://data.cityofchicago.org
