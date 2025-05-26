import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def generate_plotly_chart(df, question):
   
    try:
        
        if hasattr(df, 'to_html'):
            
            chart_html = create_chart_based_on_data(df, question)
        else:
            
            chart_html = f"<pre>{str(df)}</pre>"
            
        return chart_html
    
    except Exception as e:
        print(f"Error generating chart: {str(e)}")
        return f"<div class='error'>Error generating visualization: {str(e)}</div>"

def create_chart_based_on_data(df, question):
    
    question = question.lower()
    num_columns = len(df.columns)
    
    
    if df.empty:
        return "<div>No data available for visualization</div>"
    
    
    if 'distribution' in question or 'histogram' in question:
        
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            fig = px.histogram(df, x=numeric_cols[0])
    
    elif 'correlation' in question or 'relationship' in question or 'scatter' in question:
        
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) >= 2:
            fig = px.scatter(df, x=numeric_cols[0], y=numeric_cols[1])
    
    elif 'trend' in question or 'time' in question or 'over time' in question:
        
        date_cols = [col for col in df.columns if df[col].dtype == 'datetime64[ns]' 
                     or 'date' in col.lower() or 'time' in col.lower()]
        
        numeric_cols = df.select_dtypes(include=['number']).columns
        
        if date_cols and len(numeric_cols) > 0:
            fig = px.line(df, x=date_cols[0], y=numeric_cols[0])
        elif len(numeric_cols) >= 2:
            
            fig = px.line(df, x=numeric_cols[0], y=numeric_cols[1])
    
    elif 'comparison' in question or 'compare' in question or 'bar' in question:
        
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        numeric_cols = df.select_dtypes(include=['number']).columns
        
        if categorical_cols.any() and numeric_cols.any():
            fig = px.bar(df, x=categorical_cols[0], y=numeric_cols[0])
        elif len(numeric_cols) >= 2:
            
            fig = px.bar(df, x=numeric_cols[0], y=numeric_cols[1])
    
    else:
        
        if num_columns >= 2:
            
            if len(df) > 10:
                fig = px.line(df)
            else:
                
                cat_cols = df.select_dtypes(include=['object', 'category']).columns
                x_col = cat_cols[0] if len(cat_cols) > 0 else df.columns[0]
                
                
                num_cols = df.select_dtypes(include=['number']).columns
                y_col = num_cols[0] if len(num_cols) > 0 else df.columns[1]
                
                fig = px.bar(df, x=x_col, y=y_col)
        else:
            
            fig = px.histogram(df, x=df.columns[0])
    
    
    fig.update_layout(
        title=format_question_as_title(question),
        xaxis_title=fig.layout.xaxis.title.text or "X-Axis",
        yaxis_title=fig.layout.yaxis.title.text or "Y-Axis",
        template="plotly_white"
    )
    
    return fig.to_html(full_html=False, include_plotlyjs='cdn')

def format_question_as_title(question):
    
    title = question.rstrip('?').capitalize()
    
    
    if len(title) > 600:
        title = title[:570] + '...'
        
    return title
