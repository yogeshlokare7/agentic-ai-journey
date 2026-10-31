import json
from pathlib import Path

from pydantic import ValidationError

from agentic_ai_journey.models.api_models import Customer

samples_path = Path(__file__).parent / "day4_samples.json"

with open(samples_path) as f:
    records = json.load(f)

for i, record in enumerate(records, start=1):
    try:
        customer = Customer(**record)
        print(f"Record {i}: VALID   {customer}")
    except ValidationError as e:
        problems = "; ".join(
            f"{'.'.join(str(part) for part in err['loc'])}: {err['msg']}"
            for err in e.errors()
        )
        print(f"Record {i}: INVALID {problems}")
