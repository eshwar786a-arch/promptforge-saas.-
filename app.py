from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

# Vercel environment variable se key access karne ke liye
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

def upgrade_prompt(user_prompt, category):
    frameworks = {
        "coding": f"Act as an expert Senior Developer. Optimize, refactor, and improve the following prompt to get the best coding results from an AI. Keep it structured and precise:\n\n{user_prompt}",
        "marketing": f"Act as a World-Class Copywriter and Growth Hacker. Rewrite this prompt to craft a highly persuasive, conversion-focused, and engaging marketing copy prompt:\n\n{user_prompt}",
        "creative": f"Act as an Award-Winning Author and Creative Director. Transform this prompt into an imaginative, vivid, and deeply detailed storytelling or creative writing prompt:\n\n{user_prompt}"
    }
    enhanced = frameworks.get(category, user_prompt)
    enhanced += "\n\n[Output Format: Detailed explanation followed by the optimized prompt and usage tips.]"
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
        return jsonify({"error": "Prompt khali hai"}), 400

    perfect_prompt = upgrade_prompt(raw_prompt, category)

    # Headers mein API key bilkul sahi format mein set hai
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

    return jsonify({
        "perfect_prompt": perfect_prompt,
        "ai_response": ai_response
    })
