from flask import Flask, request, jsonify
import openai
import os


openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)


#Health Check route
@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({"message": "ZenStudy backend is up and running!"})

# Generate Quiz route to generate 20 questions
@app.route('/generate-quiz', methods=['POST'])
def generate_quiz():
    data = request.get_json()
    topic = data.get("topic")

    prompt = f"""
    Generate 5 multiple-choice quiz questions for the topic "{topic}" in the following JSON format:
    {{
        "quiz": [
            {{
                "question": "What is the capital of France?",
                "options": ["A. Paris", "B. London", "C. Rome", "D. Berlin"],
                "answer": "A"
            }},
            ...
        ]
    }}
    Only return valid JSON. Do not include explanations or any other text before or after.
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    # Parse and return JSON
    try:
        import json
        raw_output = response['choices'][0]['message']['content']
        quiz_data = json.loads(raw_output)
        return jsonify(quiz_data)
    except Exception as e:
        return jsonify({"error": "Failed to parse quiz response", "details": str(e)}) 

#  Generate Mind Map from topic
@app.route('/generate-mindmap', methods=['POST'])
def generate_mindmap():
    data = request.get_json()
    topic = data.get("topic")

    prompt = f"Create a structured mind map in plain text for the topic: {topic}. Use indentation or bullet points."

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    mindmap_output = response['choices'][0]['message']['content']
    return jsonify({"mindmap": mindmap_output})

#run the app
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
app.run(host = '0.0.0.0', port=port)