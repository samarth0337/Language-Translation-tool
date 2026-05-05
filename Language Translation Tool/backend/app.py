import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
# Enable CORS so the frontend on a different port can communicate with the backend
CORS(app)

@app.route('/api/translate', methods=['POST'])
def translate():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request"}), 400

    text = data.get('text')
    source = data.get('source')
    target = data.get('target')

    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        return jsonify({"error": "Google API key is missing"}), 500

    url = f"https://translation.googleapis.com/language/translate/v2?key={api_key}"
    
    payload = {
        "q": text,
        "source": source,
        "target": target,
        "format": "text"
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()
        translated_text = result['data']['translations'][0]['translatedText']
        return jsonify({"translatedText": translated_text})
    except Exception as e:
        print("Translation error:", e)
        # If the API returned an error message, try to extract it
        if hasattr(e, 'response') and e.response is not None:
            print("API Response:", e.response.text)
        return jsonify({"error": "Translation failed"}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(port=port, debug=True)
