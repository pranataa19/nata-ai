from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Baca API key dari file
with open("api_key.txt") as f:
    api_key = f.read().strip()

# Endpoint API
endpoint = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    user_input = request.form['user_input']
    
    # Set header dan data
    headers = {
        "Content-type": "application/json"
    }
    data = {
        "contents": [{
            "parts": [{
                "text": user_input
            }]
        }]
    }

    # Kirim POST request
    response = requests.post(endpoint, headers=headers, json=data)

    if response.status_code == 200:
        response_data = response.json()
        return jsonify(response_data['candidates'][0]['content']['parts'][0]['text'])
    else:
        return jsonify({"error": response.status_code, "message": response.text}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
