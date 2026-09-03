# Automation updates for new asset parameter template
---

1. Sample data in `new_country_asset_parameters.csv` was uploaded manually based on numeric data for Japan, but as if it was for PK to test out the process

2. Profile data values are in `PK_profile_data.csv`. This is what I would expect to upload as profile data when logging into the Admin account in CMS to Add/Update new country

3. `generate_asset_template.py` is now updated to create a csv template (without defaults) to support the user workflow where entering country details and uploading profile files helps generate and download a parameter template. This is supported by a source list of assets and parameters which may be updated to fit new assets and parameters. This may later be updated to contain default parameter values as per the list for easier use.
    (a) Note that profile filename parameter values in this case would need to be internally generated based on the user input for country code, rather than the fixed default in `asset_params_list.csv`

4. 

