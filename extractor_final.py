import pytesseract
from pdf2image import convert_from_path
import re
import csv

def extract_text_from_pdf(pdf_path):
    # Convert the PDF to a list of images
    images = convert_from_path(pdf_path)

    # Initialize an empty string to store the extracted text
    extracted_text = ""
    print("=====================================================================")

    for page_number, image in enumerate(images, 1):
        # Convert each image to text using pytesseract
        extracted_text += pytesseract.image_to_string(image, lang='eng')
        print(extracted_text)
        print(type(extracted_text))
        print("=====================================================================")

    # Define the patterns to capture multiple occurrences of Name, Husband/Father Name, House Number, Age, and Gender
    patterns = [
        r"Name:\s*([A-Za-z\s]+)\s*-\s*Father's Name\s*:\s*([A-Za-z\s]+)\s*-\s*House Number\s*:\s*([\w-]+)\s*Age\s*:\s*(\d+)\s*Gender\s*:\s*(MALE|FEMALE)",
        r"Name\s*:\s*([A-Za-z\s]+)\s*-\s*(?:Father's Name|Husband's Name)\s*:\s*([A-Za-z\s]+)\s*-\s*House Number\s*:\s*(\d+)\s*Age\s*:\s*(\d+)\s*Gender\s*:\s*(MALE|FEMALE)",
        r"Name:\s*([A-Za-z\s]+)\s*-\s*Husband's Name\s*:\s*([A-Za-z\s]+)\s*-\s*House Number\s*:\s*([\w-]+)\s*Photois\s*\|\|\s*Age:\s*(\d+)\s*Gender:\s*(MALE|FEMALE)",
        r"Name:\s*([A-Za-z\s]+)\s*-\s*(?:Husband's Name|Father's Name)\s*:\s*([A-Za-z\s]+)\s*-\s*House Number\s*:\s*([\w-]+)\s*Age:\s*(\d+)\s*Gender:\s*(MALE|FEMALE)",
        r"Name\s*:\s*([A-Za-z\s]+)\s*-\s*(?:Husband's Name|Father's Name|Husband's Name\s*:\s*Father's Name\s*:)?\s*([A-Za-z\s]+)\s*-\s*House Number\s*:\s*([\w-]+)\s*Age\s*:\s*(\d+)\s*Gender\s*:\s*(MALE|FEMALE)",
        r"Name\s*:\s*([A-Za-z\s]+)\s*-\s*(?:Husband's Name|Father's Name)\s*:\s*([A-Za-z\s]+)\s*-\s*House Number\s*:\s*([\w-]+)\s*Age\s*:\s*(\d+)\s*Gender\s*:\s*(MALE|FEMALE)",
        r"Name\s*:\s*([A-Za-z\s]+)\s*-\s*(?:Husband's Name|Father's Name)\s*:\s*([A-Za-z\s]+)\s*-\s*House Number\s*:\s*([\w\s,-]+)\s*(?:Photo is )?(?:No-S2 )?Photois \|\|Age:\s*(\d+)\s*Gender:\s*(MALE|FEMALE)",
        r"Name\s*:\s*([A-Za-z\s]+)\s*-\s*(?:Wife's Name|Husband's Name|Father's Name|Mother's Name)\s*:\s*([A-Za-z\s]+)\s*-\s*House Number\s*:\s*(?:NO\s+)?(\d+)\s*Age\s*:\s*(\d+)\s*Gender\s*:\s*(MALE|FEMALE)",
        r"Name\s*:\s*([A-Za-z\s]+)\s*-\s*Husband's Name\s*:\s*([A-Za-z\s]+)?\s*-\s*House Number\s*:\s*(\d+)\s*.*Age\s*:\s*(\d+)\s*Gender\s*:\s*(MALE|FEMALE)",
        r"Name\s*:\s*([A-Za-z\s]+)\s*(?:\n|\s*)\n?\s*Father's Name\s*:\s*([A-Za-z\s]+)\s*(?:\n|\s*)\n?\s*House Number\s*:\s*([\w-]+)\s*(?:\n|\s*)\n?\s*Age\s*:\s*(\d+)\s*(?:\n|\s*)\n?\s*Gender\s*:\s*(MALE|FEMALE)",
        r"Name\s*:\s*([A-Za-z\s]+)\s*Father's Name\s*:\s*([A-Za-z\s]+)\s*House Number\s*:\s*([\w-]+)\s*Photo\s*is\s*\|\|\s*Age\s*:\s*(\d+)\s*Gender\s*:\s*(MALE|FEMALE)",
        r"Name\s*:\s*([A-Za-z\s]+)\s*-\s*(?:Husband's Name|Father's Name|Husband's Name =)\s*:\s*([A-Za-z\s]+)\s*-\s*House Number\s*:\s*([\w\s/]+)\s*Age\s*:\s*(\d+)\s*Gender\s*:\s*(MALE|FEMALE)"
    ]

    # Find all occurrences of each pattern in the complete extracted text
    all_matches = []
    for pattern in patterns:
        matches = re.findall(pattern, extracted_text)
        all_matches.extend(matches)

    # Define the output CSV file name
    output_csv_file = "output.csv"

    # Read the existing data from the CSV file
    existing_data = []
    try:
        with open(output_csv_file, mode="r", newline="") as file:
            reader = csv.DictReader(file)
            existing_data = list(reader)
            print(existing_data)

    except FileNotFoundError:
        pass

    # Append new data to the existing data
    for match in all_matches:
        name, parent_name, house_number, age, gender = map(str.strip, match)
        new_data = {"Name": name, "Parent's/Husband's Name": parent_name, "House Number": house_number, "Age": age,
                    "Gender": gender}
        existing_data.append(new_data)
        print(new_data)

    # Write the combined data (existing + new) to the CSV file
    with open(output_csv_file, mode="w", newline="") as file:
        fieldnames = ["Name", "Parent's/Husband's Name", "House Number", "Age", "Gender"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(existing_data)

    print("CSV file has been updated successfully!")

pdf_path = 'Harsha/ac016050.pdf'
extracted_text = extract_text_from_pdf(pdf_path)
