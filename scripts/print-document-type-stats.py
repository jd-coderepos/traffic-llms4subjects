import os
import xml.etree.ElementTree as ET
from collections import Counter

def parse_genre_and_type_counts(input_dir):
    # Initialize a counter for genre and type code combinations
    genre_type_counter = Counter()

    # Traverse each XML file in the directory
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".xml"):
            file_path = os.path.join(input_dir, file_name)

            try:
                # Parse the XML file
                tree = ET.parse(file_path)
                root = tree.getroot()

                # Find the document genre and type codes
                genre_code = root.find(".//documentGenreCode")
                type_code = root.find(".//documentTypeCode")

                if genre_code is not None and type_code is not None:
                    # Create a tuple for the genre and type code combination
                    combination = (genre_code.text, type_code.text)
                    genre_type_counter[combination] += 1

            except ET.ParseError as e:
                print(f"Error parsing {file_path}: {e}")

    # Print the counts of unique genre and type code combinations
    print("Counts of unique genre and document type code combinations:")
    for (genre_code, type_code), count in genre_type_counter.items():
        print(f"Genre Code: {genre_code}, Document Type Code: {type_code} - Count: {count}")

# Specify the input directory containing the XML files
input_directory = "C:\\Users\\dsouzaj\\Desktop\\Datasets\\tib-subject-indexing\\TIB-traffic-records\\"

# Run the parser
parse_genre_and_type_counts(input_directory)
