'''
Convert *.jsonl files to *.excel files. 
All files are under './train' as well as './val' folder. 
Store converted files under './train_excel' and './val_excel' folder.

We must run this script before extracting the code snippets from the excel files!
'''

import json
import pandas as pd
import os

def jsonl_to_excel(jsonl_file, fine_name, excel_folder):
    # Reads every lines and assign them into a list depends on the programming language
    data_py, data_cpp, data_c, data_other = [], [], [], []
    
    # If there is no folder for the programming language, create one.
    if not os.path.exists(os.path.join(excel_folder, 'python')):
        os.makedirs(os.path.join(excel_folder, 'python'))
    if not os.path.exists(os.path.join(excel_folder, 'cpp')):
        os.makedirs(os.path.join(excel_folder, 'cpp'))
    if not os.path.exists(os.path.join(excel_folder, 'c')):
        os.makedirs(os.path.join(excel_folder, 'c'))
    if not os.path.exists(os.path.join(excel_folder, 'other')):
        os.makedirs(os.path.join(excel_folder, 'other'))
    
    with open(jsonl_file, 'r') as f:
        lines = f.readlines()
       
    # Extract the programming language from the file name 
    for line in lines:
        line = json.loads(line)
        file_name = line.get('file_name', '')
        extension = file_name.split('.')[-1].lower()
        if extension == 'py':
            data_py.append(line)
        elif extension == 'cpp' or extension == 'cc':
            data_cpp.append(line)
        elif extension == 'c':
            data_c.append(line)
        else:
            data_other.append(line)
    
    # Convert the list into a pandas dataframe
    df_py = pd.DataFrame(data_py)
    df_cpp = pd.DataFrame(data_cpp)
    df_c = pd.DataFrame(data_c)
    df_other = pd.DataFrame(data_other)
    
    # Write the dataframe into an excel file for Python, which is under "train_excel" or "val_excel" folder.
    # If there is no such a folder, create one.
    python_save_path = os.path.join(excel_folder, 'python', fine_name[:-6] + '.xlsx')
    cpp_save_path = os.path.join(excel_folder, 'cpp', fine_name[:-6] + '.xlsx')
    c_save_path = os.path.join(excel_folder, 'c', fine_name[:-6] + '.xlsx')
    other_save_path = os.path.join(excel_folder, 'other', fine_name[:-6] + '.xlsx')
    
    df_py.to_excel(python_save_path, index=False)
    df_cpp.to_excel(cpp_save_path, index=False)
    df_c.to_excel(c_save_path, index=False)
    df_other.to_excel(other_save_path, index=False)
            

def main():
    for folder in ['train', 'val']:
        jsonl_folder = os.path.join('.', folder)
        excel_folder = os.path.join('.', folder + '_xlsx')
        if not os.path.exists(excel_folder):
            os.makedirs(excel_folder)
        for file in os.listdir(jsonl_folder):
            if file.endswith('.jsonl'):
                jsonl_file = os.path.join(jsonl_folder, file)
                jsonl_to_excel(jsonl_file, file, excel_folder)

if __name__ == '__main__':
    main()