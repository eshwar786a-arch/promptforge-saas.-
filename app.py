from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# ⚠️ Apni Groq API Key yahan paste karein
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

def upgrade_prompt(user_prompt, category):
    frameworks = {
        "coding": f"Act as an expert Senior Developer. Follow clean code principles, optimize for performance, and handle edge cases. Task: {user_prompt}",
        "marketing": f"Act as a World-Class Copywriter. Use the AIDA framework, emotional hooks, and clear CTA. Task: {user_prompt}",
        "creative": f"Act as an Award-Winning Author. Use vivid imagery and show-don't-tell technique. Task: {user_prompt}"
    }
    enhanced = frameworks.get(category, user_prompt)
    enhanced += "\n\n[Output Format: Detailed explanation followed by clean implementation.]"
    return enhanced

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.json
    raw_prompt = data.get('prompt', '')
    category = data.get('category', 'coding')
    
    if not raw_prompt:
        return jsonify({"error": "Prompt khali hai!"}), 400
        
    perfect_prompt = upgrade_prompt(raw_prompt, category)
    
    # Direct HTTP Request (No Groq library required)
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messages": [
            {
                "role": "user",
                "content": perfect_prompt
            }
        ],
        "model": "llama3-8b-8192"
    }
    
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=15
        )
        if response.status_code == 200:
            ai_response = response.json()['choices'][0]['message']['content']
        else:
            ai_response = f"API Error (Status {response.status_code}): {response.text}"
    except Exception as e:
        ai_response = f"Connection error: {str(e)}"
    
    api_ready_link = f"https://api.yourdomain.com/v1/execute?prompt={raw_prompt[:10]}..."
    
    return jsonify({
        "perfect_prompt": perfect_prompt,
        "ai_response": ai_response,
        "api_endpoint": api_ready_link
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
