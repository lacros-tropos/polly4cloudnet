# polly4cloudnet

`concat_pollyxt_files.py` provides a routine for combining the attenuated backscatter at 1064 nm and the calibrated volume depolarization at 532 nm from the [
Pollynet_Processing_Chain](https://github.com/PollyNET/Pollynet_Processing_Chain) into one daily file.

This script is only working for location 'Mindelo' at the moment.

### Usage
The python script now can be used with arg-parsing as follows:
```
python3 concat_pollyxt_files.py {timestamp} {location} {input_path} {output_path}
```
i.e.:
```
python3 concat_pollyxt_files.py '20210912' 'Mindelo' '.' '.'
```

Detailed help will be shown with:
```
python3 concat_pollyxt_files.py --help
```

### Output format

An example for the current output format is provided in [output_format.txt](output_format.txt)
