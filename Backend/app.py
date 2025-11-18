from flask import Flask, request, jsonify

# Initialize the Flask application
app = Flask(__name__)

# Define a route for the root of the API
@app.route('/')
def index():
    return "Hello from the AI Lawyer Backend!"

# Define a route to handle future API calls (e.g., for summarizing text)
# We will build this out later
@app.route('/api/summarize', methods=['POST'])
def summarize_text():
    # For now, it just returns a placeholder response
    data = request.get_json()
    text = data.get('text', '')
    
    # In the future, AI logic will go here to process the text
    summary = f"This is a summary of the text: {text[:30]}..."
    
    return jsonify({'summary': summary})

# Run the app
if __name__ == '__main__':
    # Using port 5001 to avoid potential conflicts with other services
    app.run(debug=True, port=5001)