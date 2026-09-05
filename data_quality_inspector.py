import os
import json


def load_records(file_name):
  records = []

  if os.path.exists(file_name):
    with open(file_name, "r") as file:
      records = json.load(file)

  return records

# -------------------------
# LAYER 1: STRUCTURAL CHECK
# -------------------------
def check_required_fields(records, required_fields):
  structurally_complete_records = []
  incomplete_records = []

  for record in records:
    missing_fields = []

    for field in required_fields:
      if field not in record:
        missing_fields.append(field)

    if missing_fields:
      failure_report = {
        "record": record,
        "missing_fields": missing_fields,
        "reason": "missing required fields"
      }

      incomplete_records.append(failure_report)

    else:
      structurally_complete_records.append(record)

  return structurally_complete_records, incomplete_records

# -------------------------
# LAYER 2: VALUE / TYPE CHECK
# -------------------------
def check_types(structurally_complete_records, expected_types):
  type_valid_records = []
  invalid_type_records = []

  for record in structurally_complete_records:
    type_errors = []

    for field, expected_type in expected_types.items():
      value = record[field]

      if value is None:
        type_errors.append(field)

      elif isinstance(value, str) and value.strip() == "":
        type_errors.append(field)

      elif not isinstance(value, expected_type):
        type_errors.append(field)

    if type_errors:
      failure_report = {
        "record": record,
        "invalid_fields": type_errors,
        "reason": f"Invalid types: {type_errors}"
      }

      invalid_type_records.append(failure_report)
    else:
      type_valid_records.append(record)

  return type_valid_records, invalid_type_records

# -------------------------
# LAYER 3: PHYSICS CHECK
# -------------------------
def check_physics(type_valid_records):
  physically_valid_records = []
  physically_invalid_records = []

  for record in type_valid_records:
    physics_errors = []
    temp = record["temperature"]
    physics_error = {
      "field": "temperature",
      "value": temp
    }

    if temp < 0:
      physics_errors.append(physics_error)

    if physics_errors:
      failure_report = {
        "record": record,
        "invalid_fields": physics_errors,
        "reason": f"Invalid physics: {physics_errors}"
      }

      physically_invalid_records.append(failure_report)

    else:
      physically_valid_records.append(record)

  return physically_valid_records, physically_invalid_records

# -------------------------
# LAYER 4: VALID INSTRUMENTATION READING
# -------------------------
def check_instrument_reading(physically_valid_records, instrument_limits):
  instrument_invalid_records = []
  instrument_valid_records = []

  for record in physically_valid_records:
    temp = record["temperature"]

    min_temp = instrument_limits["temperature"]["min"]
    max_temp = instrument_limits["temperature"]["max"]

    if temp < min_temp or temp > max_temp:
      failure_report = {
        "record": record,
        "invalid_fields": "temperature",
        "value": temp,
        "reason": f"Temperature outside instrument range: {min_temp}-{max_temp} K"
      }

      instrument_invalid_records.append(failure_report)

    else:
      instrument_valid_records.append(record)

  return instrument_valid_records, instrument_invalid_records

# -------------------------
# LAYER 5: EXPECTED
# -------------------------
def check_expected_range(instrument_valid_records, expected_ranges):
  expected_range_records = []
  review_records = []

  for record in instrument_valid_records:
    temp = record["temperature"]

    min_temp = expected_ranges["temperature"]["min"]
    max_temp = expected_ranges["temperature"]["max"]

    if temp < min_temp or temp > max_temp:
      review_report = {
        "record": record,
        "review_field": "temperature",
        "value": temp,
        "reason": f"Please review, temperature outside anticipated range: {min_temp}-{max_temp} K"
      }

      review_records.append(review_report)

    else:
      expected_range_records.append(record)

  return expected_range_records, review_records

def main():
  project_name = "Data Quality Inspector"
  file_name = "records.json"

  records = load_records(file_name)

  # Validation rules
  required_fields = [
    "trial_id",
    "voltage",
    "current",
    "temperature",
  ]

  expected_types = {
    "trial_id": str,
    "voltage": (int, float),
    "current": (int, float),
    "temperature": (int, float),
  }

  instrument_limits = {
    "temperature": {
      "min": 250,
      "max": 350
    }
  }

  expected_ranges = {
    "temperature": {
      "min": 290,
      "max": 310
    }
  }

  # LAYER 1
  structurally_complete_records, incomplete_records = check_required_fields(
    records,
    required_fields
  )

  # LAYER 2
  type_valid_records, invalid_type_records = check_types(
    structurally_complete_records,
    expected_types
  )

  # LAYER 3
  physically_valid_records, physically_invalid_records = check_physics(
    type_valid_records
  )

  # LAYER 4
  instrument_valid_records, instrument_invalid_records = check_instrument_reading(
    physically_valid_records,
    instrument_limits
  )

  # LAYER 5
  expected_range_records, review_records = check_expected_range(
    instrument_valid_records,
    expected_ranges
  )


  print("\nStructurally complete records:")
  print(json.dumps(structurally_complete_records, indent=2))

  print("\nStructurally incomplete records:")
  print(json.dumps(incomplete_records, indent=2))

  print("\nInvalid type records:")
  print(json.dumps(invalid_type_records, indent=2))

  print("\nType-valid records:")
  print(json.dumps(type_valid_records, indent=2))

  print("\nPhysically invalid records:")
  print(json.dumps(physically_invalid_records, indent=2))

  print("\nPhysically valid records:")
  print(json.dumps(physically_valid_records, indent=2))

  print("\nInstrument invalid records:")
  print(json.dumps(instrument_invalid_records, indent=2))

  print("\nInstrument valid records:")
  print(json.dumps(instrument_valid_records, indent=2))

  print("\nReview records:")
  print(json.dumps(review_records, indent=2))

  print("\nExpected range records:")
  print(json.dumps(expected_range_records, indent=2))
if __name__ == "__main__":
  main()