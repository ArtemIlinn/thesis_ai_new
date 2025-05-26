import pandas as pd
import PyPDF2
import json
import os

def get_file_content(file_path, file_type, preview=False):
    
    try:
        if file_type == 'csv':
            df = pd.read_csv(file_path)
            if preview:
                return df.head(5).to_string()
            return df
        
        elif file_type == 'pdf':
            content = ""
            with open(file_path, 'rb') as f:
                pdf_reader = PyPDF2.PdfReader(f)
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    content += page.extract_text() + "\n"
            return content
        
        elif file_type == 'txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        
        elif file_type == 'json':
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
                
    except Exception as e:
        return f"Error reading file: {str(e)}"

def process_csv_data(file_path):
    
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        print(f"Error processing CSV: {str(e)}")
        return None
