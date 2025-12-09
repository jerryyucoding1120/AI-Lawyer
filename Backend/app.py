import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# --- All the setup code remains the same ---
def find_best_model():
    print("\n" + "="*50)
    print("🔍 Searching for available Gemini models...")
    available_models = []
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)
        if 'models/gemini-2.5-pro' in available_models:
            print("➡️ Selected model: 'gemini-2.5-pro'")
            return 'gemini-2.5-pro'
        if 'models/gemini-2.5-flash' in available_models:
            print("➡️ Selected model: 'gemini-2.5-flash'")
            return 'gemini-2.5-flash'
        if 'models/gemini-pro-latest' in available_models:
            print("➡️ Selected model: 'gemini-pro-latest'")
            return 'gemini-pro-latest'
        return None
    except Exception as e:
        print(f"🚨 Could not list models: {e}")
        return None
    finally:
        print("="*50 + "\n")

try:
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
    if not GEMINI_API_KEY: raise ValueError("GEMINI_API_KEY env var not set.")
    genai.configure(api_key=GEMINI_API_KEY)
    MODEL_NAME = find_best_model()
    if MODEL_NAME:
        model = genai.GenerativeModel(MODEL_NAME)
        print(f"✅ Gemini model '{MODEL_NAME}' configured.")
    else:
        raise ValueError("Could not find a suitable model.")
except Exception as e:
    print(f"🚨 Error during initial setup: {e}")
    model = None

# --- Flask App ---
app = Flask(__name__)
CORS(app)

@app.route('/api/summarize', methods=['POST'])
def get_answer():
    if model is None: return jsonify({'error': 'AI model not configured.'}), 503

    data = request.get_json()
    question = data.get('text', '')
    if not question: return jsonify({'error': 'No question provided.'}), 400

    prompt = (
        "You are a helpful legal AI assistant. "
        "Answer the following question in a clear, concise manner, limiting your response to 2-3 sentences. "
        f"Question: {question}"
    )
    
    try:
        # --- UPDATED: max_output_tokens is now 1600 ---
        generation_config = {"max_output_tokens": 1600, "temperature": 0.7}
        
        safety_settings = {
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        }

        response = model.generate_content(
            prompt,
            generation_config=generation_config,
            safety_settings=safety_settings
        )

        if response.parts:
            answer = "".join(part.text for part in response.parts)
        else:
            reason = "UNKNOWN"
            if response.candidates and response.candidates[0].finish_reason:
                reason = response.candidates[0].finish_reason.name
            
            if reason == "MAX_TOKENS":
                answer = "The AI's response was too long and had to be cut short. This can happen with complex questions."
            else:
                answer = f"The AI's response was blocked. (Reason: {reason})"
        
        return jsonify({'summary': answer})

    except Exception as e:
        print(f"Error during Gemini API call: {e}")
        return jsonify({'error': f'Failed to generate answer from Gemini: {e}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)