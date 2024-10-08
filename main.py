from flask import Flask, send_from_directory, render_template, jsonify, request
import json
import forced_alignment
import os

app = Flask(__name__)

# Ensure the temp directory exists
TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)

'''
Route to render the index.html template when accessing the root URL.
'''
@app.route('/')
def index():
    return render_template('index.html')

'''
Route to serve audio files located in the 'temp' directory based on the provided filename.
'''
@app.route('/temp/<filename>', endpoint='audio')
def audio(filename):
    return send_from_directory(TEMP_DIR, filename)

'''
Route to retrieve text data from files and return it in JSON format with corresponding intervals.
'''
@app.route('/api/get_text')
def get_text():
    with open(os.path.join(TEMP_DIR, "myFile.txt"), "r", encoding='utf-8') as question:
        text = question.read().split("\n")
    with open(os.path.join(TEMP_DIR, "syncmap.json"), "r", encoding='utf-8') as interval:
        data = json.load(interval)
        intervals = [float(fragment["begin"]) for fragment in data["fragments"]]
    response = [[intervals[i], text[i]] for i in range(len(intervals))]
    return jsonify(response)

'''
Route to retrieve the next question based on specified question numbers, subjects, and reading speed parameters.
'''
@app.route('/api/get_next_question', methods=['GET'])
def get_next_question():
    question_numbers = request.args.getlist('question_numbers')[0]
    if len(question_numbers) > 2:
        question_numbers = [int(number) for number in ''.join([char for char in question_numbers if char not in [';', ':', '!', "*", " ", "[", "]",'"']]).split(",")]
    subjects = request.args.getlist('subjects')[0]
    reading_speed = float(request.args.getlist('readingSpeed')[0].replace('"',''))
    print(f"Question Numbers: {question_numbers}")
    print(f"Subjects: {subjects}")
    if len(question_numbers) > 2 and len(subjects) > 2:
        forced_alignment.generate_sync_map(question_numbers=question_numbers, subjects=subjects, reading_speed=reading_speed)
    elif len(question_numbers) > 2:
        forced_alignment.generate_sync_map(question_numbers=question_numbers, reading_speed=reading_speed)
    elif len(subjects) > 2:
         forced_alignment.generate_sync_map(subjects=subjects, reading_speed=reading_speed)
    else:
        forced_alignment.generate_sync_map(reading_speed=reading_speed)
    return "Done"

'''
Route to retrieve the answer from a text file.
'''
@app.route('/api/get_answer')
def get_answer():
    with open(os.path.join(TEMP_DIR, "answer.txt"), "r", encoding='utf-8') as answer:
        return answer.read()

# The block below is no longer needed as Gunicorn will start the server.
if __name__ == '__main__':
    # app.run(debug=True)
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)