import os
import xml.etree.ElementTree as ET

def strip_namespaces(element):
    """Removes all namespaces from the tags of an XML element and its children."""
    for elem in element.iter():
        if '}' in elem.tag:
            elem.tag = elem.tag.split('}', 1)[1]  # Remove namespace
    return element

def extract_individual_records(input_dir, output_dir):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Traverse all files in the input directory
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".xml"):
            file_path = os.path.join(input_dir, file_name)
            print(f"Processing file: {file_path}")

            try:
                # Parse the XML file
                tree = ET.parse(file_path)
                root = tree.getroot()

                # Define namespace dictionary
                namespaces = {'oai': 'http://www.openarchives.org/OAI/2.0/'}

                # Iterate over each <record> element within the XML file
                for record in root.findall(".//oai:record", namespaces):
                    # Retrieve the identifier from <header> for filename
                    identifier = record.find(".//oai:identifier", namespaces)
                    if identifier is not None:
                        record_id = identifier.text.split(":")[-1]  # Use last part of identifier as filename
                        output_file = os.path.join(output_dir, f"{record_id}.xml")

                        # Strip namespaces from the record
                        clean_record = strip_namespaces(record)

                        # Write the individual record to a new XML file
                        with open(output_file, 'wb') as f:
                            f.write(b'<?xml version="1.0" encoding="UTF-8" ?>\n')
                            ET.ElementTree(clean_record).write(f, encoding="utf-8", xml_declaration=False)
                        print(f"Record {record_id} saved to {output_file}")

                    else:
                        print(f"No identifier found for a record in {file_name}")

            except ET.ParseError as e:
                print(f"Error parsing {file_path}: {e}")

# Specify the input and output directories
input_directory = "C:\\Users\\dsouzaj\\Desktop\\Datasets\\tib-subject-indexing\\TIB-traffic-reports-raw-data\\"
output_directory = "C:\\Users\\dsouzaj\\Desktop\\Datasets\\tib-subject-indexing\\TIB-traffic-records\\"

# Run the extraction
extract_individual_records(input_directory, output_directory)
