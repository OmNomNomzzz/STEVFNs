#!/usr/bin/env python3
"""
Create an empty country-assets input template from asset_params_list.csv.

The generated file contains every asset/parameter combination from the
parameter list, preserves the parameter-list order, copies the unit, and
leaves country-specific values and source/note fields empty.

Usage:
    python generate_asset_template.py
    python generate_asset_template.py --input asset_params_list.csv \
        --output new_country_assets_input_template.csv
"""

import argparse
from pathlib import Path
import pandas as pd


OUTPUT_COLUMNS = [
    "asset_name",
    "location_name",
    "parameter_name",
    "parameter_value",
    "unit",
    "source(s)",
    "note",
    "suggested_new_value",
    "new_source",
    "new_note",
]


def create_template(input_csv: Path, output_csv: Path) -> None:
    params = pd.read_csv(input_csv)

    required_columns = {"asset_name", "parameter_name", "unit"}
    missing = required_columns - set(params.columns)
    if missing:
        raise ValueError(
            f"Missing required column(s) in {input_csv}: "
            + ", ".join(sorted(missing))
        )

    template = pd.DataFrame({
        "asset_name": params["asset_name"],
        "location_name": "",
        "parameter_name": params["parameter_name"],
        "parameter_value": "",
        "unit": params["unit"],
        "source(s)": "",
        "note": "",
        "suggested_new_value": "",
        "new_source": "",
        "new_note": "",
    })

    template.to_csv(output_csv, index=False)

    print(f"Created: {output_csv}")
    print(f"Rows: {len(template)}")
    print(f"Assets: {template['asset_name'].nunique()}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create an empty new_country_assets_input.csv template."
    )
    parser.add_argument(
        "--input",
        default="asset_params_list.csv",
        type=Path,
        help="Path to asset_params_list.csv",
    )
    parser.add_argument(
        "--output",
        default="new_country_assets_input_template.csv",
        type=Path,
        help="Path for the generated template CSV",
    )
    args = parser.parse_args()

    create_template(args.input, args.output)


if __name__ == "__main__":
    main()