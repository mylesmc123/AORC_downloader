# This script can be used to download hourly AORC precip data from the web.
# It is currently setup to download from the AORC_LMRFC_4km repository for Hurricane Ida Aug 26, 2021 – Sep 4, 2021.
# The zip files are compressed hourly netCDF files by month.
# Ex: AORC_APCP_4KM_LMRFC_202101.zip will contain every hourly netcdf file for January, 2021.

import zipfile
import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta
import glob, os

stormName = "Ida"
outDir = rf"C:\Class\Day 1\Workshop Files\Python for Model Data\AORC_Precip\{stormName}"
# Convert string date to to datetime objects for iterating
startDate = datetime.strptime("28AUG2021", "%d%b%Y")
endDate = datetime.strptime("01SEP2021", "%d%b%Y")

# Iterate by months from startdate to endDate
date = startDate
while date < (endDate + relativedelta(months=+1)):
    # Convert date to format needed for URL
    date_str = datetime.strftime(date, "%Y%m")
    # Download each days zip file.
    URL = f"https://hydrology.nws.noaa.gov/aorc-historic/AORC_LMRFC_4km/LMRFC_precip_partition/AORC_APCP_4KM_LMRFC_{date_str}.zip"
    response = requests.get(URL, verify=False)
    open(f"AORC_APCP_4KM_LMRFC_{date_str}.zip", "wb").write(response.content)
    
    # Unzip hourly netCDF files to a single directory. 
    with zipfile.ZipFile(f"AORC_APCP_4KM_LMRFC_{date_str}.zip", 'r') as zip_ref:
        zip_ref.extractall(outDir)
    
    # Go to next day
    date = date + relativedelta(months=+1)

# Trim unzipped data to start - end dates
for file in os.listdir(outDir):
    # Get all *.nc4 files
    if file.endswith(".nc4"):
        filepath = os.path.join(outDir, file)
        # get the date string
        filedate = file.split(".")[0][-10:-2]
        # convert the date string to a datetime object
        filedate_dt = datetime.strptime(filedate, "%Y%m%d")
        # delete file if date of the file is out of our starDate to EndDate range.
        if (filedate_dt < startDate) or (filedate_dt > endDate):
            os.remove(filepath)
        
