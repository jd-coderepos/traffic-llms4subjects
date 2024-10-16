import os
import xml.etree.ElementTree as ET
import json
import csv
from collections import defaultdict

# Paths to directories and files
xml_dir = 'C:\\Users\\dsouzaj\\Desktop\\Datasets\\traffic-llms4subjects\\data\\'
taxonomy_json_path = 'C:\\Users\\dsouzaj\\Desktop\\Datasets\\llms4subjects\\shared-task-datasets\\GND\\dataset\\GND-Subjects-all.json'
mapped_output_csv = 'C:\\Users\\dsouzaj\\Desktop\\Datasets\\traffic-llms4subjects\\data-stats\\mapped_subjects.csv'
unmapped_output_csv = 'C:\\Users\\dsouzaj\\Desktop\\Datasets\\traffic-llms4subjects\\data-stats\\unmapped_subjects.csv'

# Load the GND taxonomy from JSON
with open(taxonomy_json_path, 'r', encoding='utf-8') as json_file:
    gnd_taxonomy = json.load(json_file)

# Convert GND taxonomy to a dictionary for quick lookup by Code, stripping "gnd:" prefix
gnd_dict = {entry['Code'].replace('gnd:', ''): entry['Name'] for entry in gnd_taxonomy}

# Dictionary to count occurrences of each (id, name) pair
subject_counts = defaultdict(int)

# Parse XML files to extract gnd subjects and their frequency
for xml_file in os.listdir(xml_dir):
    if xml_file.endswith('.xml'):
        # Parse XML file
        tree = ET.parse(os.path.join(xml_dir, xml_file))
        root = tree.getroot()

        # Find all "subject" elements of type "gnd"
        for subject in root.findall('.//subject[@type="gnd"]'):
            # Get the "id" attribute and the subject name
            subject_id = subject.get('id', None)
            subject_name = subject.findtext('subject')
            
            # Only add valid (id, name) pairs
            if subject_id and subject_name:
                subject_counts[(subject_id, subject_name)] += 1

# Lists to store mapped and unmapped subjects with frequency
mapped_subjects = []
unmapped_subjects = []

# Separate subjects into mapped and unmapped based on GND taxonomy
for (subject_id, subject_name), count in subject_counts.items():
    # Check if the stripped subject_id exists in the GND taxonomy
    if subject_id in gnd_dict and gnd_dict[subject_id] == subject_name:
        mapped_subjects.append((subject_id, subject_name, count))
    else:
        unmapped_subjects.append((subject_id, subject_name, count))

# Sort both lists by frequency in descending order
mapped_subjects.sort(key=lambda x: x[2], reverse=True)
unmapped_subjects.sort(key=lambda x: x[2], reverse=True)

# Write the mapped subjects to CSV
with open(mapped_output_csv, mode='w', newline='', encoding='utf-8') as mapped_file:
    writer = csv.writer(mapped_file)
    writer.writerow(['id', 'subject_name', 'frequency'])
    writer.writerows(mapped_subjects)

# Write the unmapped subjects to CSV
with open(unmapped_output_csv, mode='w', newline='', encoding='utf-8') as unmapped_file:
    writer = csv.writer(unmapped_file)
    writer.writerow(['id', 'subject_name', 'frequency'])
    writer.writerows(unmapped_subjects)

print("Mapping complete. Check the output CSV files for results, sorted by frequency in descending order.")
