How to cite:

Please cite all the references in "CITATIONS.bib" file.

How to install:

The STEVFNs tool has the following dependencies:
1. cvxpy
https://www.cvxpy.org/install/index.html
conda install -c conda-forge cvxpy

2. pandas
https://pandas.pydata.org/docs/getting_started/install.html
conda install pandas

3. matplotlib
https://matplotlib.org/stable/users/installing/index.html
conda install matplotlib

How to run:

A demo and tutorial for using the STEVFNs tool can be found on Aniq's youtube channel. This is part of a seminar for the STEVFNs tool.
https://www.youtube.com/watch?v=_n2w6Zzfofw

Details of how assets are modelled in STEVFNs is given in the STEVENs asset model seminar:
https://www.youtube.com/watch?v=caSYzciVFKw

If you do not wish to watch the long video tutorial, please follow the following.

To run the base example, run the main.py file in your IDE of choice. This runs an example of the energy system used by the case study in Aniq Ahsan's DPhil thesis, but for 4 days instead of a full year.

To change the scenario:
1. Open Data/Case_Study/SG_Case_Study/scenario_0/Asset_Parameters.csv
2. Change the value in the "asset type" column for the asset that you wish to change. This should be a number that is defined as an asset brand.
3. Open Data/Case_Study/SG_Case_Study/scenario_0/Location_Parameters.csv
4. Change the values of the lat and lon for the respective locations.
5. The main branch only contains PV and WIND data for the following locations:
	(0,0); (30,30); (30,-30); (-30,30); (-30,-30)
6. To use a different location, make sure you add more RE profiles for the locations in the RE asset code folder.

To make a new scenario:
1. Duplicate (copy and paste) a scenario folder, e.g. the Data/Case_Study/SG_Case_Study/scenario_0 folder in the Data/Case_Study/SG_Case_Study folder
2. Make relevant changes to the scenario.

To check and add a new brand type for an asset:
1. Open Code/Assets/insert_asset_name/parameters.csv For example, for the EL_Transport asset: Code/Assets/EL_Transport/parameters.csv
2. Add a new line. Make sure the numbers in the "Type" column increase from 0, 1, 2, etc.
3. The units are just for reference, they do not affect the code.
4. Make sure all values columns are filled.
6. You can now use the "Type" number for the new asset brand when changing scenario parameters.

To change case study:
1. Open Data/Case_Study/SG_Case_Study/Network_Structure.csv
2. Add or remove lines with assets.
3. Make sure the "Asset_Number" column goes from 0,1,2,3,... 
4. Copy the "Asset_NUmber", "Asset_Class", "Location_1" and "Location_2" columns to all the scenario "Asset_Parameters.csv" files. Make sure the scenarios have brand types defined for all assets.

To make a new case study:
1. Duplicate (copy and paste) a case study folder, e.g. the Data/Case_Study/SG_Case_Study folder in the Data/Case_Study folder
2. Make relevant changes to the case study.
3. Make relevant changes to scenarios.
4. Open main.py
5. Replace case_study_name from "SG_Case_Study" to the name of the name of the new case study folder.
6. e.g. if the new case study folder is "Aniq_Case_Study", replace the line:
	case_study_name = "SG_Case_Study"
  with the line:
	case_study_name = "Aniq_Case_Study"


