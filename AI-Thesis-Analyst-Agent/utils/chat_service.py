import os
import json
import requests
from utils.data_processor import get_file_content, process_csv_data
from utils.code_executor import execute_pandas_code
from utils.visualization import generate_plotly_chart

# Configure models based on your specific APIs
MODELS = {
    'deepseek': {
        'api_url': 'YOUR_DEEPSEEK_API_URL',
        'api_key': 'YOUR_DEEPSEEK_API_KEY'
    },
    'qwen': {
        'api_url': 'YOUR_QWEN_API_URL',
        'api_key': 'YOUR_QWEN_API_KEY'
    },
    'yandexGPT': {
        'api_url': 'YOUR_YANDEX_API_URL',
        'api_key': 'YOUR_YANDEX_API_KEY'
    }
}


def chat_respond(question, user_files_path, model='deepseek'):
    
    # 1. Extract content from uploaded files
    file_contents = {}
    csv_files = []
    pdf_contents = []
    
    for filename in os.listdir(user_files_path):
        file_path = os.path.join(user_files_path, filename)
        if filename.endswith('.csv'):
            csv_files.append(file_path)
            # Store a preview for context
            file_contents[filename] = get_file_content(file_path, 'csv', preview=True)
        elif filename.endswith('.pdf'):
            pdf_content = get_file_content(file_path, 'pdf')
            pdf_contents.append(pdf_content)
            file_contents[filename] = "PDF document loaded"
        elif filename.endswith(('.txt', '.json')):
            file_contents[filename] = get_file_content(file_path, os.path.splitext(filename)[1][1:])
    
    # 2. Prepare context for the LLM
    context = f"""
    User question: {question}
    
    Available files:
    {json.dumps(file_contents, indent=2)}
    
    PDF contents summary:
    {' '.join(pdf_contents)[:2000]}  # Limit context size
    """
    
    # 3. Get text answer from LLM
    text_response = query_llm(context, model=model)  # Or use any model preference logic
    
    # 4. If a CSV file is available, ask LLM to generate pandas code for analysis
    chart_html = ""
    if csv_files:
        code_prompt = f"""
        Based on the user's question: "{question}"
        
        Generate Python pandas code to analyze the following CSV files:
        {', '.join([os.path.basename(f) for f in csv_files])}
        
        The code should:
        1. Load the CSV data
        2. Process and aggregate as needed
        3. Create a plotly visualization that answers the question
        4. Return only the pandas and plotly code without explanations
        
        Here's a preview of the data:
        {json.dumps({os.path.basename(f): file_contents[os.path.basename(f)] for f in csv_files}, indent=2)}
        """
        
        pandas_code = query_llm(code_prompt, model=model, response_type='code')
        
        # 5. Execute generated pandas code safely
        df_result = execute_pandas_code(pandas_code, csv_files)
        
        # 6. Generate plotly visualization
        if df_result is not None:
            chart_html = generate_plotly_chart(df_result, question)
    
    return text_response, chart_html

def query_llm(prompt, model='deepseek', response_type='text'):
    
    model_config = MODELS.get(model, MODELS['deepseek'])
    
   
    try:
        
        headers = {
            'Authorization': f"Bearer {model_config['api_key']}",
            'Content-Type': 'application/json'
        }
        
        data = {
            'prompt': prompt,
            'max_tokens': 1000,
            'temperature': 0.3 if response_type == 'code' else 0.7
        }
        
        response = requests.post(model_config['api_url'], headers=headers, json=data)
        response.raise_for_status()
        
       
        result = response.json().get('choices', [{}])[0].get('text', '')
        return result.strip()
        
    except Exception as e:
        print(f"Error querying LLM: {str(e)}")
        return "I encountered an error while processing your request."
