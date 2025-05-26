import pandas as pd
import os
import ast
from io import StringIO
import sys
import traceback

def execute_pandas_code(code_string, csv_files):
    
    file_dict = {os.path.basename(f): f for f in csv_files}
    
    
    safe_globals = {
        'pd': pd,
        'os': os,
        'file_dict': file_dict,
        'print': print,
    }
    
    
    old_stdout = sys.stdout
    mystdout = StringIO()
    sys.stdout = mystdout
    
    result_df = None
    
    try:
       
        processed_code = preprocess_code(code_string, file_dict)
        
       
        exec(processed_code, safe_globals)
        
        
        if 'result_df' in safe_globals:
            result_df = safe_globals['result_df']
        
    except Exception as e:
        print(f"Error executing code: {str(e)}")
        traceback.print_exc()
    finally:
        
        sys.stdout = old_stdout
    
    return result_df

def preprocess_code(code_string, file_dict):
    
    for filename, filepath in file_dict.items():
        code_string = code_string.replace(f'"{filename}"', f'file_dict["{filename}"]')
        code_string = code_string.replace(f"'{filename}'", f'file_dict["{filename}"]')
    
   
    if 'result_df' not in code_string:
        
        lines = code_string.split('\n')
        df_candidates = []
        
        for line in lines:
            if 'fig' in line and '.plot(' in line:
                parts = line.split('.plot(')
                if parts and parts[0].strip():
                    df_candidates.append(parts[0].strip())
        
        
        if df_candidates:
            code_string += f"\nresult_df = {df_candidates[-1]}"
    
    return code_string
