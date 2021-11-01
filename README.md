# polly4cloudnet

`concat_pollyxt_files.py` provides a routine for combining the attenuated backscatter at 1064 nm and the calibrated volume depolarization at 532 nm from the [
Pollynet_Processing_Chain](https://github.com/PollyNET/Pollynet_Processing_Chain) into one daily file.

This script is only working for location 'Mindelo' at the moment.

### Usage
The python script now can be used with arg-parsing as follows:
```
python3 concat_pollyxt_files.py --help

usage: concat_pollyxt_files.py [-h] [-t timestamp] [-l location] [-i input_path] [-o output_path]

Concatenate pollyxt nc-files (att_backscattering@1064nm and vol_depol@532nm) from one day, with input variables: timestamp, location, input_path, output_path

optional arguments:
  -h, --help            show this help message and exit
  -t timestamp, --timestamp timestamp
                        input the timestamp of pollyxt measurement
  -l location, --location location
                        input the location/site of pollyxt measurement
  -i input_path, --input_path input_path
                        set the absolute input path to the polly dataset; if not set, the script tries to find the correct dataset from timestamp and location input
  -o output_path, --output_path output_path
                        set the absolute output path for the resulting, concatenated nc-file
```
i.e.:
```
python3 concat_pollyxt_files.py -t '20210912' -l 'Mindelo' -i '.' -o '.'
```

### Output format

An example for the current output format is provided in [output_format.txt](output_format.txt)
