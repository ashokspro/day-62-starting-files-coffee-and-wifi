import os
import pandas as pd

# File path to the Excel file
FILE_PATH = 'C:/Users/ashok/Desktop/DEMORRESULT.xlsx'

# Subject and credit mapping
SUBJECT_CREDITS = {
    'CCS336': 4,
    'CCS345': 2,
    'CCS354': 3,
    'CCS356': 3,
    'CCW332': 3,
    'IT3681': 2,
    'MX3089': 2,
    'NM1007': 3
}

# Grade-to-points mapping
GRADE_POINTS = {
    'O': 10, 'A+': 9, 'A': 8, 'B+': 7, 'B': 6, 'RA': 0, 'U': 0,
    'UA': 0, 'W': 0, 'I': 0, 'WH': 0, 'WH1': 0
}

# Extract data from the Excel file
def extract_data_from_excel(file_path):
    data = []
    try:
        # Check if file exists
        if not os.path.exists(file_path):
            print(f"Error: File not found at {file_path}")
            return []

        # Read the Excel file, skipping the first row
        df = pd.read_excel(file_path, header=1)  # Use the second row as header (index=1)

        # Identify subject columns dynamically
        subject_columns = [col for col in df.columns if col.startswith("Grade")]

        # Loop through each row in the DataFrame
        for _, row in df.iterrows():
            reg_number = str(row.get('Reg. Number', '')).strip()
            name = str(row.get('Stud. Name', '')).strip()

            # Extract grades dynamically based on subject columns
            grades = []
            for subject_col in subject_columns:
                grade = row.get(subject_col, '').strip()  # Get the grade for the subject
                subject = subject_col  # Use the column name as the subject name

                # Assign credit from SUBJECT_CREDITS or default to 3
                credit = SUBJECT_CREDITS.get(subject, 3)

                if grade:  # Only include valid grades
                    grades.append({
                        'subject': subject,
                        'grade': grade,
                        'credit': credit
                    })

            if reg_number and name:  # Ensure valid registration number and name
                data.append({
                    'Reg. Number': reg_number,
                    'Name': name,
                    'Grades': grades
                })

        return data
    except Exception as e:
        print(f"Error extracting data from Excel: {e}")
        return []

# Main script execution
if __name__ == "__main__":
    # Extract data
    extracted_data = extract_data_from_excel(FILE_PATH)

    # Print the extracted data
    if extracted_data:
        print("Extracted Data:")
        for student in extracted_data:
            print(student)
    else:
        print("No valid data extracted.")
import tensorflow as tf