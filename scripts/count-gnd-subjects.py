import os
import csv
import xml.etree.ElementTree as ET
from collections import Counter

def count_gnd_subjects(input_dir, output_file):
    # Initialize a counter for subjects with type="gnd" using (id, name) as the key
    gnd_subject_counter = Counter()

    # Traverse each XML file in the directory
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".xml"):
            file_path = os.path.join(input_dir, file_name)

            try:
                # Parse the XML file
                tree = ET.parse(file_path)
                root = tree.getroot()

                # Find all <subject> elements with type="gnd"
                for subject in root.findall(".//subject[@type='gnd']"):
                    # Extract the id attribute and the text content within the <subject> element
                    subject_id = subject.get("id")
                    subject_name = subject.find("subject").text if subject.find("subject") is not None else None
                    
                    # Only count if both id and name are present
                    if subject_id and subject_name:
                        gnd_subject_counter[(subject_id, subject_name)] += 1

            except ET.ParseError as e:
                print(f"Error parsing {file_path}: {e}")

    # Write the output to a CSV file in descending order of occurrences
    with open(output_file, "w", encoding="utf-8", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["ID and Subject Name", "Occurrences"])  # Header row

        # Sort items by occurrences in descending order and write to CSV
        for (subject_id, subject_name), count in gnd_subject_counter.most_common():
            writer.writerow([f"{subject_id} - {subject_name}", count])

    print(f"Results written to {output_file}")

# Specify the input directory and output file
input_directory = "C:\\Users\\dsouzaj\\Desktop\\Datasets\\traffic-llms4subjects\\data\\"
output_file = "C:\\Users\\dsouzaj\\Desktop\\Datasets\\traffic-llms4subjects\\data-stats\\gnd_subject_counts.csv"

# Run the counting function
count_gnd_subjects(input_directory, output_file)
