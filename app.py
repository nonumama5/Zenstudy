from flask import Flask, request, jsonify
import openai
from dotenv import load_dotenv
import os



load_dotenv() #LOADING ENVIRONMENTAL VARIABLES FROM ENV FILE
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

    prompt = f"Create 20 multiple choice quiz questions with 4 options and answers for the topic: {topic}."

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    quiz_output = response['choices'][0]['message']['content']
    return jsonify({"quiz": quiz_output})

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