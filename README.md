# Data Quality Inspector

A Python pipeline for validating experimental data through structural, type, physics, instrument, and expected-range checks.

## Overview

Data Quality Inspector processes experimental records through a five-layer validation pipeline. Each layer checks a different aspect of data quality before routing the record to one of three final outcomes:

- **Accepted** — passes all validation layers
- **Review** — valid data that falls outside the expected experimental range
- **Rejected** — fails a structural, type, physical, or instrument constraint

The project is designed around the idea that unusual scientific data should not automatically be discarded. Measurements that are technically valid but unexpected are routed for human review instead.

## Validation Pipeline

Each record moves through the pipeline in order:

1. **Structural validation**
   - Confirms all required fields are present.

2. **Type and value validation**
   - Rejects missing, blank, or incorrectly typed values.

3. **Physics validation**
   - Checks whether measurements are physically possible.
   - For example, temperature below `0 K` is rejected.

4. **Instrument validation**
   - Confirms measurements fall within the configured instrument operating range.

5. **Expected-range validation**
   - Flags measurements that are valid but outside the anticipated experimental range.
   - These records are sent to **Review** rather than rejected.

## Data Model

Each experimental record requires:

```json
{
  "trial_id": "T001",
  "voltage": 5.0,
  "current": 0.01,
  "temperature": 295.0
}
```

Required field types:

- `trial_id` — string
- `voltage` — integer or float
- `current` — integer or float
- `temperature` — integer or float, measured in Kelvin

Current validation rules:

- Physical temperature minimum: `0 K`
- Instrument temperature range: `250–350 K`
- Expected temperature range: `290–310 K`

These validation rules are currently defined in the application and can be configured or extended in future versions.

## Running the Inspector

From the project directory:

```bash
python3 data_quality_inspector.py
```

The program reads:

```text
records.json
```

After the validation pipeline runs, a QA summary is printed to the terminal.

Processed results are written to:

```text
inspection_results.json
```

Rejected and review records include additional diagnostic information explaining why each record was routed to that category.

## Testing

The project includes regression, edge-case, integration, boundary, and file-output tests using `pytest`.

Run the test suite with:

```bash
python -m pytest -q
```

The current test suite includes:

- missing required fields
- multiple missing fields
- invalid Python types
- `None` and blank values
- physically impossible measurements
- instrument-range violations
- exact instrument boundary values
- expected-range review routing
- full five-layer pipeline routing
- JSON output creation and structure

File-output testing uses pytest temporary directories so the application's real output files are not overwritten during testing.

## Project Structure

```text
data_quality_inspector/
├── data_quality_inspector.py
├── records.json
├── test_data_quality_inspector.py
├── .gitignore
└── README.md
```

## Future Development

Possible extensions include:

- configurable validation rules
- additional voltage and current constraints
- derived quantities such as resistance (`R = V / I`)
- richer QA reporting
- ingestion of larger experimental datasets
- downstream signal and anomaly analysis

A future Signal Hunter project could consume the validated output produced by this pipeline.