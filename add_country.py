"""
Script to add a new country to the STEVFNs model.
This involves updating location parameters, processing assets (demand and RE profiles),
setting up case study folders (BAU, Least Cost, Autarky), and running initial simulations.
"""

import os
import shutil
import subprocess
import sys

import pandas as pd


def add_new_country():
    """
    Main function to add a new country based on 'new_country_input.csv'.
    Updates global location parameters and triggers asset/case study processing.
    """
    # File paths
    input_csv_path = "new_country_input.csv"
    location_params_path = "Data/Case_Study/0_BASEAUTARKY/BAU/Location_Parameters.csv"

    # Check if input file exists
    if not os.path.exists(input_csv_path):
        print(f"Error: {input_csv_path} not found.")
        return

    # Read input data
    try:
        new_country_df = pd.read_csv(input_csv_path)
    except Exception as e:
        print(f"Error reading {input_csv_path}: {e}")
        return

    if new_country_df.empty:
        print("Error: Input CSV is empty.")
        return

    # Read existing location parameters
    try:
        location_params_df = pd.read_csv(location_params_path)
    except Exception as e:
        print(f"Error reading {location_params_path}: {e}")
        return

    # Build mapping of existing countries to their IDs
    existing_country_ids = {}
    for _, loc_row in location_params_df.iterrows():
        existing_country_ids[str(loc_row["location_name"])] = loc_row["Location"]

    # Separate new vs existing countries and build country_id_map
    new_countries_list = []
    existing_countries_list = []
    country_id_map = {}

    for _, row in new_country_df.iterrows():
        country_code = str(row["country_code"])
        if country_code in existing_country_ids:
            existing_countries_list.append(row)
            country_id_map[country_code] = existing_country_ids[country_code]
            print(
                f"Country {country_code} already exists (Location ID: {existing_country_ids[country_code]}). Will update."
            )
        else:
            new_countries_list.append(row)

    # Get the last location ID for new countries
    if not location_params_df.empty:
        last_id = location_params_df["Location"].max()
    else:
        last_id = -1

    # Process new countries - assign new IDs
    new_locations = []
    for row in new_countries_list:
        new_id = last_id + 1
        last_id = new_id
        country_code = str(row["country_code"])
        country_id_map[country_code] = new_id

        new_entry = {
            "Location": new_id,
            "lat": row["lat"],
            "lon": row["lon"],
            "location_name": country_code,
        }
        new_locations.append(new_entry)
        print(f"Added {country_code} with Location ID: {new_id}")

    # Update existing countries in the dataframe
    for row in existing_countries_list:
        country_code = str(row["country_code"])
        location_params_df.loc[
            location_params_df["location_name"].astype(str) == country_code, "lat"
        ] = row["lat"]
        location_params_df.loc[
            location_params_df["location_name"].astype(str) == country_code, "lon"
        ] = row["lon"]
        print(f"Updated {country_code} coordinates: lat={row['lat']}, lon={row['lon']}")

    # Save updated location parameters (includes updates to existing countries)
    if existing_countries_list:
        location_params_df.to_csv(location_params_path, index=False)
        print(
            f"Updated {len(existing_countries_list)} existing locations in {location_params_path}"
        )

    # Append new locations
    if new_locations:
        new_locations_df = pd.DataFrame(new_locations)
        # Ensure columns match
        new_locations_df = new_locations_df[location_params_df.columns]

        # Check if file ends with newline
        with open(location_params_path, "rb+") as f:
            f.seek(0, 2)  # Seek to end of file
            if f.tell() > 0:
                f.seek(-1, 2)
                last_char = f.read(1)
                if last_char != b"\n":
                    f.write(b"\n")

        # Append to file
        new_locations_df.to_csv(
            location_params_path, mode="a", header=False, index=False
        )
        print(
            f"Successfully added {len(new_locations)} new locations to {location_params_path}"
        )

    # Process assets
    assets_csv_path = "new_country_assets_input.csv"
    if os.path.exists(assets_csv_path):
        process_assets(assets_csv_path, new_country_df)

    # Process BAU_No_Action
    process_case_study_folder(new_country_df, country_id_map, "BAU_No_Action")
    # Process Least_Cost_Emissions
    process_case_study_folder(new_country_df, country_id_map, "Least_Cost_Emissions")

    # Run Simulations
    print("\nRunning BAU_No_Action simulation...")
    try:
        subprocess.run([sys.executable, "run_cases.py", "bau"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running BAU simulation: {e}")

    print("\nRunning Least_Cost_Emissions simulation...")
    try:
        subprocess.run([sys.executable, "run_cases.py", "least"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running Least Cost simulation: {e}")

    # Run Carbon Budget Generation
    print("\nGenerating Carbon Budget...")
    try:
        # Run generate_carbon_budget.py and pass 'n' to the prompt
        # Script expects to be run from Code/Automations due to relative paths
        automations_dir = os.path.join(os.getcwd(), "Code", "Automations")
        subprocess.run(
            [sys.executable, "generate_carbon_budget.py"],
            input="n\n",
            text=True,
            check=True,
            cwd=automations_dir,
        )
    except subprocess.CalledProcessError as e:
        print(f"Error running Carbon Budget generation: {e}")

    # Process Autarky Case Study
    process_autarky_case(new_country_df, country_id_map)

    # Run Update Scripts
    print("\nRunning Update Scripts...")
    automations_dir = os.path.join(os.getcwd(), "Code", "Automations")

    # Run update_aut_scenarios.py
    for _, row in new_country_df.iterrows():
        country_code = row["country_code"]
        print(f"Running update_aut_scenarios.py for {country_code}...")
        try:
            subprocess.run(
                [sys.executable, "update_aut_scenarios.py", country_code],
                check=True,
                cwd=automations_dir,
            )
        except subprocess.CalledProcessError as e:
            print(f"Error running update_aut_scenarios.py: {e}")

    # Run update_co2_budget_asset_types.py
    print("Running update_co2_budget_asset_types.py...")
    try:
        subprocess.run(
            [sys.executable, "update_co2_budget_asset_types.py"],
            check=True,
            cwd=automations_dir,
        )
    except subprocess.CalledProcessError as e:
        print(f"Error running update_co2_budget_asset_types.py: {e}")

    # Run Autarky Simulation
    for _, row in new_country_df.iterrows():
        country_code = row["country_code"]
        print(f"\nRunning Autarky simulation for {country_code}...")
        try:
            subprocess.run(
                [sys.executable, "run_cases.py", country_code],
                check=True,
                cwd=os.getcwd(),
            )
        except subprocess.CalledProcessError as e:
            print(f"Error running Autarky simulation for {country_code}: {e}")

    # Run Prepare Data for Website
    print("\nRunning prepare_data_for_website.py...")
    try:
        subprocess.run(
            [sys.executable, "prepare_data_for_website.py"],
            check=True,
            cwd=automations_dir,
        )
    except subprocess.CalledProcessError as e:
        print(f"Error running prepare_data_for_website.py: {e}")


def process_autarky_case(new_country_df, country_id_map):
    """
    Sets up the Autarky case study folder for the new country by copying
    from the base template and updating location/asset parameters. If the
    Autarky folder already exists, updates in place instead of recreating.
    """
    base_source_dir = "Data/Case_Study/0_BASEAUTARKY"

    if not os.path.exists(base_source_dir):
        print(
            f"Warning: Source directory {base_source_dir} not found. Skipping Autarky processing."
        )
        return

    for _, row in new_country_df.iterrows():
        country_code = str(row["country_code"])
        country_id = country_id_map.get(country_code)

        if country_id is None:
            print(
                f"Warning: No ID found for {country_code}, skipping Autarky processing."
            )
            continue

        target_dir = os.path.join("Data/Case_Study", f"Autarky_{country_code}")

        # Check if directory already exists
        if os.path.exists(target_dir):
            print(f"Autarky folder {target_dir} already exists. Updating in place.")
        else:
            # Copy directory from template only for new countries
            shutil.copytree(base_source_dir, target_dir)
            print(f"Copied Autarky case from {base_source_dir} to {target_dir}")

        # Update Network_Structure.csv
        net_struct_path = os.path.join(target_dir, "Network_Structure.csv")
        if os.path.exists(net_struct_path):
            try:
                df = pd.read_csv(net_struct_path)
                df["Location_1"] = country_id
                df["Location_2"] = country_id
                df.to_csv(net_struct_path, index=False)
                print(f"Updated {net_struct_path}")
            except Exception as e:
                print(f"Error updating {net_struct_path}: {e}")

        # Update BAU/Asset_Parameters.csv
        bau_asset_path = os.path.join(target_dir, "BAU", "Asset_Parameters.csv")
        if os.path.exists(bau_asset_path):
            try:
                df = pd.read_csv(bau_asset_path)
                df["Location_1"] = country_id
                df["Location_2"] = country_id
                # Change Asset_Type to country_id where Asset_Class is not CO2_Budget
                df.loc[df["Asset_Class"] != "CO2_Budget", "Asset_Type"] = country_id
                # Ensure Asset_Type is integer
                df["Asset_Type"] = df["Asset_Type"].astype(int)
                df.to_csv(bau_asset_path, index=False)
                print(f"Updated {bau_asset_path}")
            except Exception as e:
                print(f"Error updating {bau_asset_path}: {e}")


def process_case_study_folder(new_country_df, country_id_map, folder_name):
    """
    Copies a standard case study folder (e.g., BAU_No_Action) from a source country (JP)
    to the new country and updates its parameters. If the country folder already exists,
    updates the parameters in place instead of copying from template.
    """
    base_dir = os.path.join("Data/Case_Study", folder_name)
    source_country = "JP"

    if not os.path.exists(os.path.join(base_dir, source_country)):
        print(
            f"Warning: Source directory {os.path.join(base_dir, source_country)} not found. Skipping {folder_name} processing."
        )
        return

    import shutil

    for _, row in new_country_df.iterrows():
        country_code = str(row["country_code"])
        country_id = country_id_map.get(country_code)

        if country_id is None:
            print(
                f"Warning: No ID found for {country_code}, skipping {folder_name} processing."
            )
            continue

        target_dir = os.path.join(base_dir, country_code)

        # Check if directory already exists
        if os.path.exists(target_dir):
            print(f"Country folder {target_dir} already exists. Updating in place.")
        else:
            # Copy directory from template only for new countries
            shutil.copytree(os.path.join(base_dir, source_country), target_dir)
            print(f"Copied {folder_name} from {source_country} to {country_code}")

        # Update Asset_Parameters.csv
        asset_params_path = os.path.join(target_dir, "Asset_Parameters.csv")
        if os.path.exists(asset_params_path):
            try:
                df = pd.read_csv(asset_params_path)
                # Change Asset_Type to country_id where Asset_Class is not CO2_Budget
                df.loc[df["Asset_Class"] != "CO2_Budget", "Asset_Type"] = country_id
                # Ensure Asset_Type is integer
                df["Asset_Type"] = df["Asset_Type"].astype(int)
                df.to_csv(asset_params_path, index=False)
                print(f"Updated {asset_params_path}")
            except Exception as e:
                print(f"Error updating {asset_params_path}: {e}")

        # Update Location_Parameters.csv
        loc_params_path = os.path.join(target_dir, "Location_Parameters.csv")
        if os.path.exists(loc_params_path):
            try:
                df = pd.read_csv(loc_params_path)
                # Update lat, lon, location_name
                # Location ID should remain 0 as per user request
                # df['Location'] = country_id
                df["lat"] = row["lat"]
                df["lon"] = row["lon"]
                df["location_name"] = country_code
                df.to_csv(loc_params_path, index=False)
                print(f"Updated {loc_params_path}")
            except Exception as e:
                print(f"Error updating {loc_params_path}: {e}")


def infer_re_type(asset_name):
    """
    Infers the RE_type (PVOUT or WINDOUT) for a renewable energy asset from its
    name, so the tidy input template no longer needs to carry an explicit
    RE_type column. Only assets whose name starts with 'RE' are considered
    renewable assets.
    """
    if not asset_name.upper().startswith("RE"):
        return None
    name_upper = asset_name.upper()
    if "PV" in name_upper:
        return "PVOUT"
    elif "WIND" in name_upper:
        return "WINDOUT"
    return None


def round_re_coords(lat, lon):
    """
    Rounds lat/lon onto the RE profile grid (0.5 degree steps for latitude,
    0.625 degree steps for longitude), matching the resolution of the
    underlying RE profile datasets (e.g. MERRA-2 derived PVOUT/WINDOUT grids).
    """
    import numpy as np

    r_lat = np.int64(np.round((lat) / 0.5)) * 0.5
    r_lat = min(r_lat, 90.0)
    r_lat = max(r_lat, -90.0)

    r_lon = np.int64(np.round((lon) / 0.625)) * 0.625
    r_lon = min(r_lon, 179.375)
    r_lon = max(r_lon, -180.0)

    return r_lat, r_lon


def load_country_profile_data(profile_data_path):
    """
    Reads a per-country profile data CSV (matching the layout of
    profile_data_template.csv): one column per profile-bearing asset
    (e.g. 'EL_Demand', 'HTH_Demand', and each individual RE_* asset name),
    plus '_Unit' companion columns for the demand assets.

    The first data row is a units row (only meaningful for the demand
    columns) and every row after that is one hour of that asset's annual
    (8760-hour) profile.

    Returns (values_df, unit_row):
      - values_df: the profile values only (unit row dropped), index reset.
      - unit_row: a pandas Series (original column labels -> unit-row value),
        used only for logging/validation, never written to any output file.
    """
    raw_df = pd.read_csv(profile_data_path, encoding="utf-8-sig")
    if raw_df.empty:
        raise ValueError(f"{profile_data_path} is empty")

    unit_row = raw_df.iloc[0]
    values_df = raw_df.iloc[1:].reset_index(drop=True)

    if len(values_df) != 8760:
        print(
            f"Warning: {profile_data_path} has {len(values_df)} profile rows "
            f"after the unit row (expected 8760)."
        )

    return values_df, unit_row


def build_param_dict(group_df):
    """
    Collapses a tidy (asset_name, location_name, parameter_name, parameter_value, unit)
    group of rows -- all rows for a single asset -- into a flat dict of
    parameter_name -> parameter_value, plus a companion dict of
    parameter_name -> unit. Numeric-looking values are converted to floats.
    """
    param_values = {}
    param_units = {}
    for _, prow in group_df.iterrows():
        pname = prow["parameter_name"]
        pval = prow["parameter_value"]
        punit = prow.get("unit")

        # Try to coerce to numeric; fall back to the raw string (e.g. profile_filename)
        try:
            pval_numeric = pd.to_numeric(pval)
            param_values[pname] = pval_numeric
        except (ValueError, TypeError):
            param_values[pname] = pval

        if pd.notna(punit):
            param_units[pname] = punit

    return param_values, param_units


def process_assets(assets_csv_path, new_country_df):
    """
    Processes asset parameters and profiles (Demand and RE) for the new country,
    reading the tidy/long-format asset input template:
        asset_name, location_name, parameter_name, parameter_value, unit, source(s), note

    Profile data (the actual hourly time series for Demand and RE assets) comes
    from a separate, parallel per-country input file named
    '<country_code>_profile_data.csv', matching the layout of
    profile_data_template.csv: one column per profile-bearing asset (e.g.
    'EL_Demand', 'HTH_Demand', and each individual RE_* asset name), plus
    '_Unit' companion columns for the demand assets. The first data row is a
    units row; every row after that is one hour of the asset's annual profile.

    For each asset in the tidy parameters template:
      - All parameter rows for that asset are collapsed into one set of parameter
        values (the template values, taken from whichever source country/location
        the template was built from, e.g. 'JP'). These values are reused as-is for
        every new country being added, exactly as the old wide-format template did.
      - EL_Demand / HTH_Demand assets: if the asset's column is present in the new
        country's profile data file, a single-column CSV with header 'Demand' is
        written to Code/Assets/<asset_name>/profiles/<country_code>_2050_GW.csv,
        and the parameters.csv 'profile_filename' field is set to the destination
        filename (without extension). The '_Unit' row value (if present) is only
        logged for a sanity check, never written to any output file.
      - RE_* assets: RE_type (PVOUT/WINDOUT) is inferred from the asset name. If
        the asset's column is present in the new country's profile data file, a
        single-column CSV with no header is written to
        Code/Assets/<asset_name>/profiles/<RE_type>/lat<r_lat>/<RE_type>_lat<r_lat>_lon<r_lon>.csv
        (lat/lon rounded onto the RE profile grid; destination-path convention
        unchanged from the original RE Asset Logic). No profile filename/path is
        written into parameters.csv for RE assets.
      - Any parameter_name with a companion 'unit' value also updates a
        '<parameter_name>_unit' or '<parameter_name>_units' column in
        parameters.csv, if such a column exists for that asset.
    """
    try:
        assets_long_df = pd.read_csv(assets_csv_path, encoding="utf-8-sig")
    except Exception as e:
        print(f"Error reading {assets_csv_path}: {e}")
        return

    if assets_long_df.empty:
        print("Warning: Assets CSV is empty.")
        return

    required_cols = {"asset_name", "location_name", "parameter_name", "parameter_value"}
    missing_cols = required_cols - set(assets_long_df.columns)
    if missing_cols:
        print(f"Error: {assets_csv_path} is missing required columns: {missing_cols}")
        return

    # Create a mapping of country code to lat/lon for the country(ies) being added
    country_coords = {}
    for _, row in new_country_df.iterrows():
        country_coords[str(row["country_code"])] = (row["lat"], row["lon"])

    # Preload each new country's profile data file (one file per country, named
    # '<country_code>_profile_data.csv', in the current working directory).
    profile_data_by_country = {}
    for country_code in country_coords:
        profile_data_path = f"{country_code}_profile_data.csv"
        if not os.path.exists(profile_data_path):
            print(
                f"Warning: {profile_data_path} not found; Demand/RE profile "
                f"files will not be generated for {country_code} (parameter "
                f"values will still be written)."
            )
            continue
        try:
            profile_data_by_country[country_code] = load_country_profile_data(
                profile_data_path
            )
        except Exception as e:
            print(f"Error reading {profile_data_path}: {e}")

    for asset_name, group in assets_long_df.groupby("asset_name"):
        asset_dir = os.path.join("Code", "Assets", asset_name)
        params_path = os.path.join(asset_dir, "parameters.csv")

        if not os.path.exists(params_path):
            print(
                f"Warning: Parameters file not found for {asset_name} at {params_path}"
            )
            continue

        try:
            params_df = pd.read_csv(params_path)
        except Exception as e:
            print(f"Error reading {params_path}: {e}")
            continue

        # Collapse this asset's tidy rows into a flat parameter_name -> value map
        param_values, param_units = build_param_dict(group)

        is_demand_asset = "Demand" in asset_name
        re_type = infer_re_type(asset_name)

        # Prepare new rows for each new/updated country
        new_rows = []
        for country_code, (lat, lon) in country_coords.items():
            new_row = dict(param_values)
            new_row["location_name"] = country_code
            new_row["set_size"] = 24
            new_row["set_number"] = 0
            country_profile = profile_data_by_country.get(country_code)

            if is_demand_asset:
                # Default year; matches prior behaviour
                year = "2050"
                dest_filename = f"{country_code}_{year}_GW.csv"
                dest_dir = os.path.join(asset_dir, "profiles")
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)
                dest_path = os.path.join(dest_dir, dest_filename)

                if "profile_filename" in params_df.columns:
                    new_row["profile_filename"] = dest_filename.replace(".csv", "")

                if country_profile is not None:
                    values_df, unit_row = country_profile
                    if asset_name in values_df.columns:
                        series = pd.to_numeric(values_df[asset_name], errors="coerce")
                        pd.DataFrame({"Demand": series.values}).to_csv(
                            dest_path, index=False
                        )
                        print(f"Wrote demand profile to {dest_path}")

                        unit_col = f"{asset_name}_Unit"
                        if unit_col in unit_row.index and pd.notna(unit_row[unit_col]):
                            print(
                                f"  Profile data unit for {asset_name} "
                                f"({country_code}): {unit_row[unit_col]}"
                            )
                    else:
                        print(
                            f"Warning: Column '{asset_name}' not found in "
                            f"{country_code}_profile_data.csv; demand profile "
                            f"file not written."
                        )

            elif re_type is not None:
                # RE Asset Logic (destination-path convention unchanged from the
                # original script's lines 443-465); RE_type is inferred from the
                # asset name rather than read from the template, and the profile
                # values come from the country's profile data file rather than
                # being copied from a source file.
                r_lat, r_lon = round_re_coords(lat, lon)

                dest_dir = os.path.join(asset_dir, "profiles", re_type, f"lat{r_lat}")
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)
                dest_filename = f"{re_type}_lat{r_lat}_lon{r_lon}.csv"
                dest_path = os.path.join(dest_dir, dest_filename)

                if country_profile is not None:
                    values_df, _unit_row = country_profile
                    if asset_name in values_df.columns:
                        series = pd.to_numeric(values_df[asset_name], errors="coerce")
                        series.to_csv(dest_path, index=False, header=False)
                        print(f"Wrote RE profile to {dest_path}")
                    else:
                        print(
                            f"Warning: Column '{asset_name}' not found in "
                            f"{country_code}_profile_data.csv; RE profile file "
                            f"not written."
                        )

                # RE assets don't carry a profile filename/path field in
                # parameters.csv; the profile file itself is located by the
                # model at runtime from the asset's rounded lat/lon.
                new_row.pop("profile_filename", None)
                new_row.pop("profile_path", None)
                new_row["RE_type"] = re_type
                new_row["set_number"] = 0
                new_row["set_size"] = 24

            # Apply units: for any parameter with a companion unit value, write it
            # into a '<param>_unit' or '<param>_units' column if that column exists
            for pname, punit in param_units.items():
                for unit_col in (f"{pname}_unit", f"{pname}_units"):
                    if unit_col in params_df.columns:
                        new_row[unit_col] = punit

            # Filter down to columns that exist in the target parameters.csv
            row_dict = {
                col: val for col, val in new_row.items() if col in params_df.columns
            }

            # Fill any target columns not covered by the template with None
            # ('Type' is handled separately below via auto-increment)
            for col in params_df.columns:
                if col not in row_dict and col != "Type":
                    row_dict[col] = None

            new_rows.append(row_dict)

        if not new_rows:
            continue

        new_rows_df = pd.DataFrame(new_rows)

        # Check which countries already exist in params_df
        existing_locations = []
        if "location_name" in params_df.columns:
            existing_locations = params_df["location_name"].astype(str).tolist()

        # Separate into rows to update vs rows to add
        rows_to_update = new_rows_df[
            new_rows_df["location_name"].isin(existing_locations)
        ]
        rows_to_add = new_rows_df[
            ~new_rows_df["location_name"].isin(existing_locations)
        ]

        # Update existing rows
        if not rows_to_update.empty:
            for _, update_row in rows_to_update.iterrows():
                loc_name = str(update_row["location_name"])
                # Update all columns except 'Type' (keep existing Type ID)
                for col in update_row.index:
                    if col in params_df.columns and col != "Type":
                        params_df.loc[
                            params_df["location_name"].astype(str) == loc_name, col
                        ] = update_row[col]
            params_df.to_csv(params_path, index=False)
            print(f"Updated {len(rows_to_update)} existing rows in {params_path}")

        # Handle Type ID auto-increment for new rows only
        if not rows_to_add.empty:
            if "Type" in params_df.columns and pd.api.types.is_numeric_dtype(
                params_df["Type"]
            ):
                start_id = params_df["Type"].max() + 1 if not params_df.empty else 0
                rows_to_add = rows_to_add.copy()
                rows_to_add["Type"] = range(start_id, start_id + len(rows_to_add))

            # Align columns
            rows_to_add = rows_to_add[params_df.columns]

            # Check for newline
            with open(params_path, "rb+") as f:
                f.seek(0, 2)
                if f.tell() > 0:
                    f.seek(-1, 2)
                    last_char = f.read(1)
                    if last_char != b"\n":
                        f.write(b"\n")

            rows_to_add.to_csv(params_path, mode="a", header=False, index=False)
            print(f"Added {len(rows_to_add)} new rows to {params_path}")


if __name__ == "__main__":
    add_new_country()