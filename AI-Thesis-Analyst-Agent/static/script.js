// static/script.js


document.getElementById('model-select').addEventListener('change', function() {
    fetch('/set_model', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `model=${encodeURIComponent(this.value)}`
    });
});






document.getElementById('user-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const userInput = document.getElementById('user-input');
    const message = userInput.value.trim();
    
    if (message) {
        // Add user message to right panel
        addMessage('user-messages', message, 'message');
        
        //
        // Send to backend
        fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `user_message=${encodeURIComponent(message)}`
        })
        .then(response => response.json())
        .then(data => {
            addBotMessage(data.bot_response, data.chart_html);
        });
        
        userInput.value = '';
    }
});


// static/script.js
function addMessage(containerId, message, className) {
    const container = document.getElementById(containerId);
    const messageDiv = document.createElement('div');
    messageDiv.className = className;
    messageDiv.textContent = message;

    if (typeof message === 'string') {
        messageDiv.innerHTML = message;
    } else {
        messageDiv.appendChild(message);
    }
    

    container.appendChild(messageDiv);
    container.scrollTop = container.scrollHeight;
}



// static/script.js - Fix file upload handler
// static/script.js - Fix file upload handler
document.getElementById('file-input').addEventListener('change', function(e) {
    const files = e.target.files;
    if (files.length === 0) return;

    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
        formData.append('files', files[i]);  // Match the Flask endpoint expectation
    }

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) throw new Error('Upload failed');
        return response.json();
    })
    .then(data => {
        if (data.success) {
            // Add newly uploaded files to the list
            const list = document.querySelector('.dataset-list');
            data.files.forEach(file => {
                const div = document.createElement('div');
                div.textContent = file;
                list.prepend(div);  // Add new files to top
            });
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('File upload failed: ' + error.message);
    });
});



// static/script.js - Update loadDatasets and initialization
// Load datasets when page loads
document.addEventListener('DOMContentLoaded', function() {
    loadDatasets();
});

// Update loadDatasets function
function loadDatasets() {
    fetch('/datasets')
        .then(response => response.json())
        .then(data => {
            const list = document.querySelector('.dataset-list');
            list.innerHTML = data.files.map(file => 
                `<div>${file}</div>`
            ).join('');
        })
        .catch(error => console.error('Error loading datasets:', error));
}





// static/script.js - Update message handling
function addBotMessage(text, chartHtml) {
    const botMessages = document.getElementById('bot-messages');
    
    // Create message container
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    
    // Add text content
    const textDiv = document.createElement('div');
    textDiv.className = 'bot-text';
    textDiv.textContent = text;
    messageDiv.appendChild(textDiv);
    
    // Add chart content
    if (chartHtml) {
        const chartContainer = document.createElement('div');
        chartContainer.className = 'plotly-chart-container '//'chart-container';
        
        // Parse and inject chart HTML
        const parser = new DOMParser();
        const doc = parser.parseFromString(chartHtml, 'text/html');
        const chartContent = doc.body.firstChild;
        
        // Clone and append chart nodes
        const importedNode = document.importNode(chartContent, true);
        chartContainer.appendChild(importedNode);
        
        // Re-execute scripts
        const scripts = chartContainer.querySelectorAll('script');
        scripts.forEach(script => {
            const newScript = document.createElement('script');
            newScript.text = script.text;
            chartContainer.appendChild(newScript);
        });
        
        messageDiv.appendChild(chartContainer);
    }
    
    botMessages.appendChild(messageDiv);
    botMessages.scrollTop = botMessages.scrollHeight;
}




function appendBotMessage(text, chartHtml = '') {
    const botMessages = document.getElementById('bot-messages');
    
    // Create message container
    const messageDiv = document.createElement('div');
    messageDiv.className = 'bot-message';
    
    // Add text element
    const textDiv = document.createElement('div');
    textDiv.className = 'bot-text';
    textDiv.textContent = text;
    
    // Add chart container
    const chartDiv = document.createElement('div');
    chartDiv.className = 'chart-container';
    
    // If chart exists, add HTML and execute scripts
    if (chartHtml) {
        chartDiv.innerHTML = chartHtml;
        const scripts = chartDiv.getElementsByTagName('script');
        for (let script of scripts) {
            const newScript = document.createElement('script');
            newScript.text = script.textContent;
            document.body.appendChild(newScript).parentNode.removeChild(newScript);
        }
    }
    
    // Assemble the message
    messageDiv.appendChild(textDiv);
    messageDiv.appendChild(chartDiv);
    botMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    botMessages.scrollTop = botMessages.scrollHeight;
}

// Modified AJAX call
document.getElementById('chat-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const userInput = document.getElementById('user-message');
    const message = userInput.value;
    
    // Add user message (you'll need to implement this)
    appendUserMessage(message); 
    
    fetch('/ask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `user_message=${encodeURIComponent(message)}`
    })
    .then(response => response.json())
    .then(data => {
        appendBotMessage(data.bot_response, data.chart_html);
        userInput.value = '';
    });
});