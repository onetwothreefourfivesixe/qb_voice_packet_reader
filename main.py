from flask import Flask, send_from_directory, render_template, jsonify, request
import json
import forced_alignment

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/<filename>')
def audio(filename):
    return send_from_directory('', filename)

@app.route('/api/get_text')
def get_text():
    # Example Python method returning data
    with open("myFile.txt", "r") as question:
        text = question.read().split("\n")
    with open("syncmap.json", "r") as interval:
        data = json.load(interval)
        intervals = [float(fragment["begin"]) for fragment in data["fragments"]]
    basic_dictionary = {intervals[i]: text[i] for i in range(len(intervals))}
    response = [{'time': float(time), 'text': text} for time, text in basic_dictionary.items()]
    response.sort(key=lambda x: x['time'])
    return jsonify(response)

@app.route('/api/get_next_question', methods=['GET'])
def get_next_question():
    question_numbers = request.args.getlist('question_numbers')[0]
    question_numbers = [int(number) for number in ''.join([char for char in question_numbers if char not in [';', ':', '!', "*", " ", "[", "]",'"']]).split(",")]
    subjects = request.args.getlist('subjects')[0]
    print(question_numbers)
    print(subjects)
    forced_alignment.generate_sync_map(question_numbers=question_numbers, subjects=subjects)
    return "Done"

@app.route('/api/get_answer')
def get_answer():
    with open("answer.txt", "r") as answer:
        return answer.read()

if __name__ == '__main__':
    app.run(debug=True)