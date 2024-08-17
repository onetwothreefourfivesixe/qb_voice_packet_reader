#Remember to uncomment the waitress code when pushing new docker images
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
    with open("myFile.txt", "r", encoding='utf-8') as question:
        text = question.read().split("\n")
    with open("syncmap.json", "r", encoding='utf-8') as interval:
        data = json.load(interval)
        intervals = [float(fragment["begin"]) for fragment in data["fragments"]]
    response = [[intervals[i], text[i]] for i in range(len(intervals))]
    return jsonify(response)

# Add this at the beginning of the file

@app.route('/api/get_next_question', methods=['GET'])
def get_next_question():
    question_numbers = request.args.getlist('question_numbers')[0]
    if len(question_numbers) > 2:
        question_numbers = [int(number) for number in ''.join([char for char in question_numbers if char not in [';', ':', '!', "*", " ", "[", "]",'"']]).split(",")]
    subjects = request.args.getlist('subjects')[0]
    reading_speed = float(request.args.getlist('readingSpeed')[0].replace('"',''))
    print(f"Question Numbers: {question_numbers}")
    print(f"Subjects: {subjects}")
    if  len(question_numbers) > 2 and len(subjects) > 2:
        forced_alignment.generate_sync_map(question_numbers=question_numbers, subjects=subjects, reading_speed=reading_speed)
    elif len(question_numbers) > 2:
        forced_alignment.generate_sync_map(question_numbers=question_numbers, reading_speed=reading_speed)
    elif len(subjects) > 2:
         forced_alignment.generate_sync_map(subjects=subjects, reading_speed=reading_speed)
    else:
        forced_alignment.generate_sync_map(reading_speed=reading_speed)
    return "Done"

@app.route('/api/get_answer')
def get_answer():
    with open("answer.txt", "r") as answer:
        return answer.read()

if __name__ == '__main__':
    # app.run(debug=True)
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)