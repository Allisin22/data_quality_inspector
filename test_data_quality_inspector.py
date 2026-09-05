from data_quality_inspector import (
  check_required_fields,
  check_types,
  check_physics,
  check_instrument_reading,
  check_expected_range
)

#Layer 1
def test_required_fields():
  required_fields = [
      "trial_id",
      "voltage",
      "current",
      "temperature",
    ]

  records = [{
      "trial_id": "T001",
      "voltage": 5.0,
      "current": .1,
      "temperature": 292,
  },
  {
      "trial_id": "T002",
      "voltage": 5.0,
      "current": .1,
  }
  ]

  structurally_complete_records, incomplete_records = check_required_fields(
    records,
    required_fields
  )

  assert len(structurally_complete_records) == 1
  assert len(incomplete_records) == 1
  assert incomplete_records[0]["missing_fields"] == ["temperature"]
  assert structurally_complete_records[0]["trial_id"] == "T001"

# LAYER 2
def test_types():
  structurally_complete_records = [
  {
    "trial_id": "T001",
    "voltage": 5.0,
    "current": 0.1,
    "temperature": 292
  },
  {
    "trial_id": "T002",
    "voltage": "five",
    "current": 0.1,
    "temperature": 292
  }
  ]

  expected_types = {
    "trial_id": str,
    "voltage": (int, float),
    "current": (int, float),
    "temperature": (int, float),
  }

  type_valid_records, invalid_type_records = check_types(
    structurally_complete_records,
    expected_types)

  assert len(type_valid_records) == 1
  assert len(invalid_type_records) == 1
  assert type_valid_records[0]["trial_id"] == "T001"
  assert invalid_type_records[0]["invalid_fields"] == ["voltage"]

# LAYER 3
def test_physics():

  type_valid_records = [
  {
    "trial_id": "T001",
    "voltage": 5.0,
    "current": 0.1,
    "temperature": 292
  },
  {
    "trial_id": "T002",
    "voltage": 4.4,
    "current": 0.1,
    "temperature": -22
  }
  ]

  physically_valid_records, physically_invalid_records = check_physics(
    type_valid_records
  )

  assert len(physically_valid_records) == 1
  assert len(physically_invalid_records) == 1
  assert physically_valid_records[0]["trial_id"] == "T001"
  assert physically_invalid_records[0]["invalid_fields"][0]["field"] == "temperature"
  assert physically_invalid_records[0]["invalid_fields"][0]["value"] == -22

# LAYER 4
def test_instrument_reading():

  instrument_limits = {
    "temperature": {
      "min": 250,
      "max": 350
    }
  }

  physically_valid_records = [
  {
    "trial_id": "T001",
    "voltage": 5.0,
    "current": 0.1,
    "temperature": 292
  },
  {
    "trial_id": "T002",
    "voltage": 4.4,
    "current": 0.1,
    "temperature": 422
  }
  ]

  instrument_valid_records, instrument_invalid_records = check_instrument_reading(
    physically_valid_records,
    instrument_limits
  )

  assert len(instrument_valid_records) == 1
  assert len(instrument_invalid_records) == 1
  assert instrument_valid_records[0]["trial_id"] == "T001"
  assert instrument_invalid_records[0]["invalid_fields"] == "temperature"
  assert instrument_invalid_records[0]["value"] == 422

# LAYER 5
def test_expected_range():

  expected_ranges = {
    "temperature": {
      "min": 290,
      "max": 310
    }
  }

  instrument_valid_records = [
  {
    "trial_id": "T001",
    "voltage": 5.0,
    "current": 0.1,
    "temperature": 292
  },
  {
    "trial_id": "T002",
    "voltage": 4.4,
    "current": 0.1,
    "temperature": 333
  }
  ]

  expected_range_records, review_records = check_expected_range(instrument_valid_records, expected_ranges)

  assert len(expected_range_records) == 1
  assert len(review_records) == 1
  assert expected_range_records[0]["trial_id"] == "T001"
  assert review_records[0]["review_field"] == "temperature"
  assert review_records[0]["value"] == 333

def test_full_pipeline():

  # Validation rules
  records = [{
    "trial_id": "T001",
    "voltage": 5.0,
    "current": .1,
    "temperature": 292,
  },
  {
    "trial_id": "T002",
    "voltage": 5.0,
    "current": .1,
  },
  {
    "trial_id": "T003",
    "voltage": "five",
    "current": 0.1,
    "temperature": 292
  },
  {
    "trial_id": "T004",
    "voltage": 5.0,
    "current": 0.1,
    "temperature": -20
  },
  {
    "trial_id": "T005",
    "voltage": 5.0,
    "current": 0.1,
    "temperature": 422
  },
  {
    "trial_id": "T006",
    "voltage": 4.4,
    "current": 0.1,
    "temperature": 333
  }
  ]

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

  assert len(expected_range_records) == 1
  assert len(incomplete_records) == 1
  assert len(invalid_type_records) == 1
  assert len(physically_invalid_records) == 1
  assert len(instrument_invalid_records) == 1
  assert len(review_records) == 1

  assert expected_range_records[0]["trial_id"] == "T001"
  assert incomplete_records[0]["record"]["trial_id"] == "T002"
  assert invalid_type_records[0]["record"]["trial_id"] == "T003"
  assert physically_invalid_records[0]["record"]["trial_id"] == "T004"
  assert instrument_invalid_records[0]["record"]["trial_id"] == "T005"
  assert review_records[0]["record"]["trial_id"] == "T006"

# LAYER 2 EDGE-CASE TEST
def test_none_and_blank_values():

  records = [{
    "trial_id": "T001",
    "voltage": 5.0,
    "current": .1,
    "temperature": 292
  },
  {
    "trial_id": "T002",
    "voltage": None,
    "current": .1,
    "temperature": 290
  },
  {
    "trial_id": "T003",
    "voltage": 4,
    "current": " ",
    "temperature": 292
  }
  ]

  expected_types = {
    "trial_id": str,
    "voltage": (int, float),
    "current": (int, float),
    "temperature": (int, float),
  }

  type_valid_records, invalid_type_records = check_types(
   records,
    expected_types
  )

  assert len(type_valid_records) == 1
  assert len(invalid_type_records) == 2
  assert type_valid_records[0]["trial_id"] == "T001"
  assert invalid_type_records[0]["record"]["trial_id"] == "T002"
  assert invalid_type_records[0]["invalid_fields"] == ["voltage"]
  assert invalid_type_records[1]["record"]["trial_id"] == "T003"
  assert invalid_type_records[1]["invalid_fields"] == ["current"]

# TEST MULTIPLE MISSING FIELDS
def test_multiple_missing_fields():

  required_fields = [
    "trial_id",
    "voltage",
    "current",
    "temperature",
  ]

  records = [{
    "trial_id": "T001",
    "voltage": 5.0,
    "current": .1,
    "temperature": 292
  },
  {
    "trial_id": "T002",
    "voltage": 4,
  }
  ]

  structurally_complete_records, incomplete_records = check_required_fields(
    records,
    required_fields
  )

  assert len(structurally_complete_records) == 1
  assert len(incomplete_records) == 1
  assert incomplete_records[0]["record"]["trial_id"] == "T002"
  assert incomplete_records[0]["missing_fields"] == ["current", "temperature"]

# TEST BOUNDARY VALUES
def test_instrument_boundaries():

  records = [{
    "trial_id": "T001",
    "voltage": 5.0,
    "current": .1,
    "temperature": 250
  },
  {
    "trial_id": "T002",
    "voltage": 5.0,
    "current": .1,
    "temperature": 350
  }
  ]

  instrument_limits = {
    "temperature": {
      "min": 250,
      "max": 350
    }
  }

  instrument_valid_records, instrument_invalid_records = check_instrument_reading(
    records,
    instrument_limits
  )

  assert len(instrument_valid_records) == 2
  assert len(instrument_invalid_records) == 0
  assert instrument_valid_records[0]["trial_id"] == "T001"
  assert instrument_valid_records[1]["trial_id"] == "T002"