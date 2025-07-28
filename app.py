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

    # Route 1: Just Questions
@app.route('/generate-questions', methods=['POST'])
def generate_questions():
    data = request.get_json()
    topic = data.get("topic")
    
    prompt = f"Give me 10 fun general knowledge questions (without answers) for the topic: {topic}. Number them."
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    questions = response['choices'][0]['message']['content']
    return jsonify({"questions": questions})

# Route 2: Questions + One-Word Answers
@app.route('/generate-answers', methods=['POST'])
def generate_answers():
    data = request.get_json()
    topic = data.get("topic")

    prompt = f"Give me 10 general knowledge questions with one-word answers for the topic: {topic}. Return as a JSON list like: {{'question': '...', 'answer': '...'}}."

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    qa_pairs = response['choices'][0]['message']['content']
    return jsonify({"quiz": qa_pairs})

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