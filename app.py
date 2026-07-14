def generate():
    data = request.json
    raw_prompt = data.get('prompt', '')
    category = data.get('category', 'coding')

    if not raw_prompt:
        return jsonify({"error": "Prompt khali hai"})

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
        "model": "llama-3.3-70b-specdec"
    }

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=15
        )
        if response.status_code == 200:
            # Aapka aage ka code yahan se start hoga...
            pass
