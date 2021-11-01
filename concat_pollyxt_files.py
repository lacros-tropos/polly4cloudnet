# -*- coding: utf-8 -*-
"""
Created on 2021-09-13

@author: Andi Klamt
"""

import numpy as np
from netCDF4 import Dataset
from pathlib import Path
import re
import datetime as dt
import sys
import argparse


### start arg parsing

## Create the parser
pollyxt_parser = argparse.ArgumentParser(description='Concatenate pollyxt nc-files (att_backscattering@1064nm and vol_depol@532nm) from one day, with input variables: timestamp, location, input_path, output_path')

## Add the arguments
pollyxt_parser.add_argument('-t', '--timestamp', dest='timestamp', metavar='timestamp',
                       type=str,
                       help='input the timestamp to look for pollyxt datasets')

pollyxt_parser.add_argument('-l', '--location', dest='location', metavar='location', #default='Mindelo',
                       type=str,
                       help='input the location/site of pollyxt measurement')

pollyxt_parser.add_argument('-i', '--input_path', dest='input_path', metavar='input_path', 
                       type=str,
                       help='set the input path to the polly datasets, i.e. "/data/level1/polly"')

pollyxt_parser.add_argument('-o', '--output_path', dest='output_path', metavar='output_path',
                       type=str,
                       help='set the output path for the concatenated nc-file')

## Execute the parse_args() method
args = pollyxt_parser.parse_args()
### end of arg parsing


### start of user defined area

## set date of measurement here:
# i.e. date_of_measurement = "20210912"
date_of_measurement = args.timestamp

## set location/site of the PollyXT here:
# i.e. location = "Mindelo"
location=args.location

## set input path o the polly datasets
# i.e. input_path="/data/level1/polly"
# the following subfolders have the structure: "{input_path}/{location}/{YYYY}/{MM}/{DD}"
# i.e. on rsd2 server the following subfolder structure for location "Mindelo" is "{input_path}/PollyXT_CPV/YYYY/MM/DD"
input_path=args.input_path

## set output path
# i.e. output_path = "/lacroshome/cloudnetpy/data/playground"
output_path = args.output_path



## INFO: call of the function main() at the end of this script has to be uncommented, to let this script work correctly!

### end of user defined area


### start of main function to call subfunctions
def main():
    # check if output path exists
    out_path=Path(output_path)
    if out_path.exists() == True:
        pass
    else:
        sys.exit("Output path does not exist. You have to create it first!")

    # check if arguments exist
    if args.location is not None and args.timestamp is not None:
        print("loc and time set")
    else:
        print("loc & time not set")
    if 'location' in globals():
        if 'date_of_measurement' in globals():
            # call of function "concat_pollyxt_files"
            concat_pollyxt_files(date_of_measurement, location, input_path, output_path)
        else:
            sys.exit("No location or date of measurement set.")
    else:
        sys.exit("No location or date of measurement set.")

    return ()
### end of main function


### start of function concat_pollyxt_files
def concat_pollyxt_files(date_of_measurement, location, input_path, output_path):
    '''
        This function locates multiple files from one day measurements (date_of_measurement: "YYYYMMDD"), containing "Attenuated backscattering" 
        and "Volume depolarization" from level 1 data at a specific site (location: i.e. "Mindelo") obtained by a PollyXT device.
        
        A single new nc file will be generated ("YYYYMMDD_location_pollyxt.nc").
        This new nc file will contain only data of the "Attenuated backscatter coefficient at 1064 nm" 
        and the "Volume depolarization ratio at 532 nm" concatenated along the time axis for this day.
        The nomenclature follows the one given from cloudnet ( https://cloudnetpy.readthedocs.io/en/latest/fileformat.html )
    '''
    
    ## generate new nc-file title
    new_file_title = date_of_measurement + "_" + location.lower() + "_pollyxt.nc"

    ## get the desired path_to_folder from "date_of_measurement" and "location"
    YYYY = date_of_measurement[0:4]
    MM   = date_of_measurement[4:6]
    DD   = date_of_measurement[6:8]

    if location == "Mindelo" or location == "mindelo":
        loc_path  = "PollyXT_CPV"
    else:
        print("No location/site found with this name.")
        sys.exit()
        
    path_to_folder = "{}/{}/{}/{}/{}".format(input_path,loc_path,YYYY,MM,DD)
    
    path_exist = Path(path_to_folder)
    if path_exist.exists() == True:
        print("\nData found for location {} on {}.".format(location,date_of_measurement))
        print("Data was found in folder: {}".format(path_to_folder))
        print("New nc file '{}' will be generated and stored to '{}'".format(new_file_title, output_path))
        print("Processing...")
    else:
        print("\nNo data found for location {} on {}.\n".format(location,date_of_measurement))
        sys.exit()
        

    ## set the searchpatterns for the att_bsc- & the vol_depol-files:
    searchpattern_att_bsc   = "*[0-9]_att*.nc"
    searchpattern_vol_depol = "*[0-9]_vol*.nc"
    
    ## get all att_bsc-files in path_to_folder
    ## and put them into a list
    
    att_bsc_files       = Path(r'{}'.format(path_to_folder)).glob('{}'.format(searchpattern_att_bsc))
    att_bsc_files_list0 = [x for x in att_bsc_files if x.is_file()]
        
    ## convert type path to type string
    att_bsc_files_list = []
    for file in att_bsc_files_list0:
        att_bsc_files_list.append(str(file))
    
    ## get all vol_depol-_files in path_to_folder
    ## and put them into a list
    vol_depol_files       = Path(r'{}'.format(path_to_folder)).glob('{}'.format(searchpattern_vol_depol))
    vol_depol_files_list0 = [x for x in vol_depol_files if x.is_file()]
        
    ## convert type path to type string
    vol_depol_files_list = []
    for file in vol_depol_files_list0:
        vol_depol_files_list.append(str(file))
    
    ## get location from global attributes
#    first_file_ds = Dataset(att_bsc_files_list[0], "r")
#    position      = 0
#    for att in first_file_ds.ncattrs():
#        if att == "location":
#            location_pos=position
#        position = position + 1
#    location = first_file_ds.getncattr(first_file_ds.ncattrs()[location_pos])
#    first_file_ds.close()
    
    ## create new filename from the splitted files
#    new_file_title = str(att_bsc_files_list[0])
#    new_file_title = re.split(r'/', new_file_title)[-1]
#    new_file_title = re.split(r'_', str(new_file_title))
#    new_file_title = new_file_title[0] + new_file_title[1] + new_file_title[2] + "_" + location.lower() + "_pollyxt.nc"
#    new_file_title = YYYY + MM + DD + location.lower() + "_pollyxt.nc"
    
    
    ## generate new nc file
    
    new_file_ds = Dataset(r"{}/{}".format(output_path, new_file_title), "w", format="NETCDF4")
    #new_file_ds = Dataset(r"{}/{}".format(path_to_folder, new_file_title), "w", format="NETCDF4")
    
    ## create dimensions
    
    # get size of time and height/range dimension
    timedimsize = 0
    for file in att_bsc_files_list:
        file_ds      = Dataset(file,"r")
        dimsize      = len(file_ds.dimensions["time"])
        timedimsize  = timedimsize+dimsize
        rangedimsize = len(file_ds.dimensions["height"])
        file_ds.close()

    # create dimension time    
    new_file_ds.createDimension("time", timedimsize)
    
    # create dimension range
    new_file_ds.createDimension("range", rangedimsize)
    
    
    ## create variables    
    
    # create variable time
    times = new_file_ds.createVariable("time","f8",("time"))
    
    # create variable range
    ranges = new_file_ds.createVariable("range","f8",("range"))
    
    # create variables 
    altitude           = new_file_ds.createVariable("altitude","int32")
    wavelength         = new_file_ds.createVariable("wavelength","int32")
    calibration_factor = new_file_ds.createVariable("calibration_factor","f8") #,("time")) # depending on time, but in the first step take the mean value of the hole day!!!
    height             = new_file_ds.createVariable("height","f8",("range")) # height = range x cos(tilt_angle)
    tilt_angle         = new_file_ds.createVariable("tilt_angle","f4")
    
    # create variable attenuated_backscatter_1064nm alias beta & vol_depol
    beta      = new_file_ds.createVariable("beta","f8",("time","range"))
    vol_depol = new_file_ds.createVariable("vol_depol","f8",("time","range"))
    

    ## set variable long names
    times.long_name              = "Time UTC"
    ranges.long_name             = "Range from instrument"
    altitude.long_name           = "Altitude of site"
    wavelength.long_name         = "Laser wavelength"
    calibration_factor.long_name = "Backscatter calibration factor"
    height.long_name             = "Height above mean sea level"
    beta.long_name               = "Attenuated backscatter coefficient at 1064 nm"
    tilt_angle.long_name         = "Tilt angle from vertical"
    vol_depol.long_name          = "Volume depolarization ratio at 532 nm"
    
    ## set units
    times.units              = "hours since {}-{}-{} 00:00:00".format(YYYY,MM,DD)
    ranges.units             = "m"
    altitude.units           = "m"
    wavelength.units         = "nm"
    beta.units               = "sr^-1 m^-1"
    vol_depol.units          = ""
    calibration_factor.units = ""
    height.units             = "m"
    tilt_angle.units         = "degrees"
    
    
    ## fill variables with values
    
    # set wavelength / nm 
    wavelength[:] = 1064
    
    # set tilt angle / degrees
    tilt_angle[:] = 5
    
    # open first nc file to get range values, altitude values and global attributes
    first_file_ds = Dataset(att_bsc_files_list[0],"r")
    
    # copy range values from first nc file (same for all files)
    ranges[:] = first_file_ds.variables["height"][:]
    
    # calc. height ... in terms of: height = range * cos(tilt_angle)
    height[:] = ranges[:] * np.cos(np.radians(tilt_angle[:]))
    
    # get and set altitude of site / meter
    altitude[:] = first_file_ds.variables["altitude"][:]
    
    
    ## append variables along time dimension
    # append from att_bsc_1064nm files
    startpos = 0
    calibration_factor_list = []
    for file in att_bsc_files_list:
        # open att_bsc nc files
        file_ds = Dataset(file,"r")
        
        # get size of time dimension of actual file
        dimsize = len(file_ds.dimensions["time"])
        
        # append time values
        times[startpos:startpos+dimsize] = file_ds.variables["time"][0:dimsize]
        
        # get SNR_1064nm and quality_mask for corrections of att_bsc (later...)
        if startpos == 0:
            SNR_all          = np.array(file_ds.variables['SNR_1064nm'])
            quality_mask_all = np.array(file_ds.variables['quality_mask_1064nm'])
        else:
            SNR              = np.array(file_ds.variables['SNR_1064nm'])
            SNR_all          = np.concatenate((SNR_all,SNR),axis=0)
            quality_mask     = np.array(file_ds.variables['quality_mask_1064nm'])
            quality_mask_all = np.concatenate((quality_mask_all,quality_mask),axis=0)
        
        # append attenuated_backscatter_1064nm values
        beta[startpos:startpos+dimsize,:] = file_ds.variables["attenuated_backscatter_1064nm"][0:dimsize,:]
        
        # get calibration_factor from all files
        position = 0
        for attribute in file_ds.variables["attenuated_backscatter_1064nm"].ncattrs():
            if attribute == "Lidar_calibration_constant_used":
                calib_pos = position
            position = position + 1
            
        calibration_factor[:] = file_ds.variables["attenuated_backscatter_1064nm"].getncattr(file_ds.variables["attenuated_backscatter_1064nm"].ncattrs()[calib_pos])
        calibration_factor_list.append(calibration_factor[:])
        
        # set new startpos for appended matrices
        startpos = startpos + dimsize
        
        # close opened nc files
        file_ds.close()
    
    
    # convert unix time (seconds since 1970-01-01) to UTC (hours since YYYY-MM-DD)
    
    #year month day - should be provided by main script (???)
    year  = int(YYYY)
    month = int(MM)
    day   = int(DD)
    
    unix_times = np.array(times)
    
    unix_to_utc = [(dt.datetime.utcfromtimestamp(s)-dt.datetime(year=year, month=month, day=day)).total_seconds()/3600 for s in unix_times]
    
    times[:] = unix_to_utc
    
    # set calibration_factor as the mean value from all files
    calibration_factor[:] = np.mean(calibration_factor_list)
            
    # append vol_depol_532nm values from vol_depol-input files
    startpos = 0
    for file in vol_depol_files_list:
        file_ds                                = Dataset(file,"r")
        dimsize                                = len(file_ds.dimensions["time"])
        vol_depol[startpos:startpos+dimsize,:] = file_ds.variables["volume_depolarization_ratio_532nm"][0:dimsize,:]
        startpos                               = startpos+dimsize
        file_ds.close()
    
    
    ## set global attributes
    
    position = 0
    for attribute in first_file_ds.ncattrs():
        if attribute == "Data Policy":
            datapolicy_pos = position
        if attribute == "location":
            location_pos   = position    
        if attribute == "source":
            source_pos     = position
        position = position + 1
        
    new_file_ds.setncattr("Data Policy", first_file_ds.getncattr(first_file_ds.ncattrs()[datapolicy_pos]))
    new_file_ds.setncattr("location", first_file_ds.getncattr(first_file_ds.ncattrs()[location_pos]))
    new_file_ds.setncattr("institute", "Leibniz Institute for Tropospheric Research (TROPOS)")
    new_file_ds.setncattr("source", first_file_ds.getncattr(first_file_ds.ncattrs()[source_pos]))

    att_bsc_files_no_path_list=[]
    for file in att_bsc_files_list:
        att_bsc_files_no_path_list.append(re.split(r'/', file)[-1])
        
    vol_depol_files_no_path_list=[]
    for file in vol_depol_files_list:
        vol_depol_files_no_path_list.append(re.split(r'/', file)[-1])

    new_file_ds.setncattr("history","this file was concatenated from att_bsc files " + str([i for i in att_bsc_files_no_path_list]) + " and from vol_depol files " + str([i for i in vol_depol_files_no_path_list]))
    
    
    # close first_file_ds
    first_file_ds.close()
    
    # close new_file_ds
    new_file_ds.close()
    
    return (print("Done!"))
### end of function concat_att_bsc_vol_depol_files


### call of main function
main()


### EOF ###
