'''
Get code snippets from xlsx file.
There are two folderss: train_xlsx and val_xlsx.
Each folder contains four subfolders: python, cpp, c, and other. And each xlsx file is named with the corresponding CWE ID, such as cwe-022.xlsx.
Save those code snippets as a code file, such as ./cwe-022/cwe-022_1.py, ./cwe-022/cwe-022_1.cpp, ./cwe-022/cwe-022_1.c, etc. We can just save the code snippets classified as other as a .txt file.
'''

import os
import pandas as pd
import re
import sys

def get_code_snippets_from_xlsx(excel_folder, code_folder):
    if not os.path.exists(code_folder):
        os.makedirs(code_folder)

    # Define the subfolders
    subfolders = ['python', 'cpp', 'c', 'other']

    # Iterate through each subfolder
    for subfolder in subfolders:
        excel_subfolder = os.path.join(excel_folder, subfolder)
        code_subfolder = os.path.join(code_folder, subfolder)

        if not os.path.exists(code_subfolder):
            os.makedirs(code_subfolder)

        # Get all xlsx files in the subfolder
        xlsx_files = [f for f in os.listdir(excel_subfolder) if f.endswith('.xlsx')]

        for xlsx_file in xlsx_files:
            cwe_id = xlsx_file.split('.')[0]  # Extract CWE ID from filename
            excel_path = os.path.join(excel_subfolder, xlsx_file)
            
            # Read the xlsx file
            df = pd.read_excel(excel_path)
            
            # Create a folder for this CWE if it doesn't exist
            cwe_folder = os.path.join(code_subfolder, cwe_id)
            if not os.path.exists(cwe_folder):
                os.makedirs(cwe_folder)
            
            # Extract and save code snippets
            for idx, row in df.iterrows():
                code_snippet = row['func_src_before']
                if pd.notna(code_snippet):
                    # Determine file extension
                    if subfolder == 'python':
                        ext = '.py'
                    elif subfolder == 'cpp':
                        ext = '.cpp'
                    elif subfolder == 'c':
                        ext = '.c'
                    else:
                        ext = '.txt'
                    
                    # Create filename
                    filename = f"{cwe_id}_{idx + 1}{ext}"
                    file_path = os.path.join(cwe_folder, filename)
                    
                    # Write code snippet to file
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(code_snippet)

    print(f"Code snippets extracted and saved in {code_folder}")

# Example usage
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <excel_folder> <code_folder>")
        sys.exit(1)
    
    excel_folder = sys.argv[1]
    code_folder = sys.argv[2]
    get_code_snippets_from_xlsx(excel_folder, code_folder)

# Example command: python get_code_snippets_from_xlsx.py train_xlsx train_code (for train), 
# python get_code_snippets_from_xlsx.py val_xlsx val_code (for val)
