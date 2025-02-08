from flask import Flask, request, jsonify, render_template
import requests
from transformers import pipeline
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ---------------------------------------------
# Configure NASA API
# ---------------------------------------------
NASA_API_BASE_URL = "https://api.nasa.gov/"
NASA_API_KEY = "tmoVZRZyIKVlyhtPjaJYgAFFOVS9hXBHBBi0hjus"  # Replace with your NASA API key

# ---------------------------------------------
# Load the Pretrained AI Model
# ---------------------------------------------
# Using Hugging Face GPT-2 pipeline for text generation
model = pipeline('text-generation', model='gpt2')  # Replace with fine-tuned model if needed

# ---------------------------------------------
# NASA API: Fetch Astronomy Picture of the Day
# ---------------------------------------------
def get_nasa_apod():
    """Fetch NASA's Astronomy Picture of the Day data."""
    endpoint = f"{NASA_API_BASE_URL}planetary/apod"
    params = {"api_key": NASA_API_KEY}
    response = requests.get(endpoint, params=params)

    if response.status_code == 200:
        return response.json()
    return {"error": "Failed to fetch data from NASA API"}

# ---------------------------------------------
# NASA API: Fetch Upcoming Space Launches
# ---------------------------------------------
def get_nasa_launches():
    """Fetch upcoming space launches from NASA API."""
    endpoint = f"{NASA_API_BASE_URL}techport/api/projects"
    params = {"api_key": NASA_API_KEY}
    response = requests.get(endpoint, params=params)

    if response.status_code == 200:
        return response.json()
    return {"error": "Failed to fetch launch data from NASA API"}

# ---------------------------------------------
# Flask Routes
# ---------------------------------------------

@app.route('/')
def home():
    """Serve the main chatbot interface."""
    return render_template('index.html')

@app.route('/question', methods=['POST'])
def handle_question():
    """
    Handle user queries by combining AI model response and NASA data.
    """
    # Extract user question from request
    data = request.get_json()
    question = data.get("question", "").strip()

    if not question:
        return jsonify({"error": "Question not provided"}), 400

    # Generate AI response
    try:
        ai_response = model(question, max_length=100, num_return_sequences=1)
        generated_text = ai_response[0]['generated_text']
    except Exception as e:
        return jsonify({"error": f"AI model error: {str(e)}"}), 500

    # Fetch NASA data
    nasa_data = get_nasa_apod()

    # Combine AI response and NASA data
    response = {
        "question": question,
        "ai_answer": generated_text,
        "nasa_data": nasa_data
    }

    return jsonify(response)

@app.route('/launches', methods=['GET'])
def get_launch_info():
    """
    Fetch and return information about upcoming space launches.
    """
    launches = get_nasa_launches()
    return jsonify(launches)

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify the backend is running.
    """
    return jsonify({"status": "Backend is running"})

# ---------------------------------------------
# Run the Flask App
# ---------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
