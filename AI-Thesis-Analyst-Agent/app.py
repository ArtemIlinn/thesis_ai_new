# app.py (Flask Backend)
from flask import Flask, render_template, request, jsonify, session
from werkzeug.utils import secure_filename
import os
import uuid
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Required for session

MODELS ={ 

    'basic': 'Qwen',
    'advanced': 'YandexGPT',
    'technical': 'DeepSeek R1'
}



def chatbot_response(user_input, model):
    # Add your model-specific logic here

    
    time.sleep(2)  # Pauses program for 2 seconds


    if model == 'basic':

        text_ = f'''
Here’s a simple plan to test a new idea (like a promo, menu item, or loyalty perk):

Pick a Goal: “Do free samples boost afternoon sales?” or “Does a new latte flavor sell better than the old one?”
Split Customers: Run the idea for half your customers (test group) and compare results to the other half (control group).
Track for 1-2 Weeks: Measure sales, repeat visits, or customer feedback.
Check Results: Did the test group perform better? If yes, roll it out. If not, tweak and retest.
Why It Works: Low risk, data-driven, and avoids guessing. Let’s brainstorm a test!
'''
        return text_


        #return f"Basic: {user_input}"
        
    elif model == 'advanced':

        text_ = f'Tier Adoption: \
        The test group (new loyalty program) showed stronger adoption of premium tiers: \
        Gold members: 9% (test) vs. 7% (control) \
        Silver members: 29% (test) vs. 18% (control) \
        This suggests the new program better incentivizes customers to reach higher tiers.\
        Engagement Gap: \
        A significant portion of customers remain Unknown (unclassified) in both groups: \
        42% (test) vs. 45% (control) \
        This indicates either low sign-up rates or unclear tier qualification criteria. \
        Bronze Tier Performance: \
        Slightly higher in the test group (21% vs. 18%), suggesting some movement from unengaged to basic loyalty.'




        text_ = f'''
                    A/B Test Results (Loyalty Onboarding):

                    Treatment Group has a lower median visits (12 vs 14) but similar average (~16) to Control.
                    Insight: New onboarding may discourage mid-frequency customers, while loyalists stay engaged.
                    Next Steps:

                    Simplify onboarding to highlight 1-2 key rewards.
                    Test a 30-day sprint with a shorter flow.
                    Analyze high vs low-frequency customer segments.
                    Recommendation: Keep the new flow for loyalists but tweak messaging for casual customers. Let’s discuss!
                    '''






        return text_
    




    elif model == 'technical':



        text__ = f'''
Here’s a breakdown of the A/B test results for the loyalty program onboarding changes. The goal was to see if the new onboarding process (treatment group) drives better loyalty tier enrollment compared to the original setup (control group). We split users during acquisition, and here’s what we found:

What’s Working Well

Fewer Customers Stuck in “Unknown” Tier 🎉
The treatment group reduced the percentage of customers without a loyalty tier from 10% to 6%—a 40% drop!
Takeaway: The new onboarding flow (e.g., clearer prompts or simplified sign-up) is likely making it easier for customers to join the program upfront.
Growth in Bronze & Silver Tiers 📈
Bronze tier enrollment increased slightly from 39% to 41% (+2%), and Silver rose from 36% to 38% (+2%).
Why It Matters: This suggests the treatment nudges customers toward entry-level tiers, which could mean stronger initial engagement.
Opportunities to Improve

Gold Tier Stagnation 🟡
Both groups have 15% of customers in Gold, meaning the treatment didn’t motivate upgrades.
Possible Reason: Gold-tier rewards might not feel exclusive or valuable enough to justify the effort to upgrade.
Small Wins, But Are They Enough? 🤔
While Bronze/Silver gains are positive, the shifts are modest (+2% each). We’ll need to track if this translates to higher spend or repeat visits.
What I Recommend

Double Down on the Onboarding Changes ✅
Roll out the treatment’s onboarding flow broadly—it’s clearly reducing "Unknown" tiers, which is a win for program adoption.
Boost Gold Tier Appeal 🏆
Test perks like “Free monthly specialty drink” or “Double points for Gold members” to incentivize upgrades.
Add a progress bar during checkout showing how close Bronze/Silver customers are to reaching Gold.
Keep an Eye on Behavior 🔍
Monitor if Bronze/Silver customers in the treatment group spend more or visit more often than control. If not, we may need to tweak tier benefits.
Test a “Fast-Track to Gold” Campaign 🚀
Offer a limited-time bonus (e.g., “Earn Gold in 3 visits instead of 5”) to see if urgency drives upgrades.
Final Thoughts

The new onboarding process is a step in the right direction for getting customers into the program, but we’re not yet seeing movement toward higher-value tiers. Let’s focus on making Gold feel irresistible while scaling the successful onboarding changes. Happy to discuss further or dive into deeper metrics!
            '''

        
        return text__ #f"Technical: {user_input}"
    





    return f"Default: {user_input}"




@app.route('/')
def index():
    session.setdefault('model', 'basic')
    return render_template('index.html', models=MODELS)

@app.route('/set_model', methods=['POST'])
def set_model():
    session['model'] = request.form['model']
    return jsonify(success=True)

@app.route('/chart')
def chart():
    session.setdefault('model', 'basic')
    return render_template('loyalty_tier_chart.html', models=MODELS)



# app.py - Modify the ask route
@app.route('/ask', methods=['POST'])
def ask():

    '''
    user_message = request.form['user_message']
    model = session.get('model', 'basic')
    
    # Generate text response
    text_response = f"{model.capitalize()} response: {user_message}"
    
    # Get Plotly HTML
    with open('/Users/artemilin/PycharmProjects/AI-Thesis-Analyst-Agent/templates/loyalty_tier_chart.html', 'r') as f:
        chart_html = f.read()
    
    # Combine text and chart
    full_response = f"""
    <div class="bot-text">{text_response}</div>
    <div class="plotly-chart-container">
        {chart_html}
    </div>
    """
    
    return jsonify({'bot_response': full_response})
    '''

    user_message = request.form['user_message']
    model = session.get('model', 'basic')
    
    # Generate text response
    #text_response = f"{model.capitalize()} response: {user_message}"
    text_response = chatbot_response(user_message, model)



    if model in  ('basic', 'Qwen'):
        chart_html = None
    # Get Plotly HTML
    elif model in  ('advanced', 'Advanced AI'):

        with open('/Users/artemilin/PycharmProjects/AI-Thesis-Analyst-Agent/box_plots.html', 'r') as f:
            
            #'/Users/artemilin/PycharmProjects/AI-Thesis-Analyst-Agent/templates/loyalty_tier_chart.html', 'r') as f:
            chart_html = f.read()

    else:
        with open('/Users/artemilin/PycharmProjects/AI-Thesis-Analyst-Agent/templates/NEW_loyalty_tier_chart.html', 'r') as f:
            chart_html = f.read()

    print('chart_html', model)

    # Generate unique ID for each chart
    #chart_id = f"chart-{uuid.uuid4().hex}"
    #chart_html = chart_html.replace("%%CHART_CONTAINER%%", chart_id)
    
    return jsonify({
        'bot_response': text_response,
        'chart_html': chart_html  # Send as separate field
    })

'''
    user_message = request.form['user_message']
    model = session.get('model', 'basic')
    
    # Generate unique chart ID
    chart_id = f"chart-{uuid.uuid4()}"
    
    return jsonify({
        'bot_response': f"{model.capitalize()} response: {user_message}",
        'chart_html': render_template(
            'loyalty_tier_chart.html',
            chart_id=chart_id
        )
    })


    id did not worked, can we just put this chat_html inside the bots respond, so it would be displayed, without any IDs, we just pass the code and visualise it in 
'''
















#### datasets

# app.py - Add these new routes

UPLOAD_FOLDER = '/Users/artemilin/PycharmProjects/AI-Thesis-Analyst-Agent/data/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# app.py - Fix upload route
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files' not in request.files:
        return jsonify(error='No files uploaded'), 400

    files = request.files.getlist('files')
    uploaded_files = []

    for file in files:
        if file.filename == '':
            continue
        if file:
            filename = secure_filename(file.filename)  # Now properly imported
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            uploaded_files.append(filename)

    if not uploaded_files:
        return jsonify(error='No valid files uploaded'), 400

    return jsonify(success=True, files=uploaded_files)


'''
@app.route('/datasets')
def list_datasets():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify(files=files)
'''

# app.py - Update the list_datasets route
@app.route('/datasets')
def list_datasets():
    files = []
    upload_path = app.config['UPLOAD_FOLDER']
    
    # Get files with their creation times
    with os.scandir(upload_path) as entries:
        for entry in entries:
            if entry.is_file():
                files.append({
                    'name': entry.name,
                    'upload_time': entry.stat().st_mtime
                })
    
    # Sort files by upload time (newest first)
    files.sort(key=lambda x: x['upload_time'], reverse=True)
    
    return jsonify(files=[f['name'] for f in files])





if __name__ == '__main__':
    app.run(debug=True)



'''
plan

create datasets 3

create message template
prompt - code (hidden) for dataframe - code (hidden) for plotly - plotly to html - to message
business insignts


create message template for a/b test post analytics

create homogeneity tests 








lets add header with logo text name on the left of the header, 

with following buttons aligned to the right: dropdown "choice of models" which will affect the response of the bot as flag in app.py, 


the "upload dataset" - which will allow us to applaud excel file

connect datasource - this will be box with input link to google sheets

.model-selector select {
    padding: 12px 20px;  /* Increased padding */
    border-radius: 16px;  /* More rounded */
    border: 2px solid #4c82af;  /* Red border */
    background-color: #4c82af;  /* Red background */
    color: white;  /* White text */
    font-size: 1em;  /* Slightly larger text */
    height: 25px;  /* Fixed height */
    transition: all 0.3s ease;
    cursor: pointer;
}
'''