Data preprocessing scripts

1. read the raw data and extract the individual records

`scripts/traffic-records-xml-parser.py --input raw-data-folder --output data`

Data statistics generation scripts

2. read the individual records and print the unique counts for document genre/type combination

`scripts/print-document-type-stats.py --input data`

3. read the individual records and print the unique gnd subjects and their occurrence counts

`scripts/count-gnd-subjects.py --input data --output data-stats/gnd_subject_counts.csv`

4. GND subject mapping and frequency analysis -- This task extracts and counts gnd subjects from XML files, maps them to the LLMs4Subjects human-readable GND taxonomy for classification validation, and outputs separate files for matched and unmatched entries with occurrence frequencies.

`scripts/validate-subjects-in-gnd.py`