#TODO: Save temp files in a temp folder
#Remember to uncomment the waitress code when pushing new docker images
from flask import Flask, send_from_directory, render_template, jsonify, request
import json
import forced_alignment
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/temp/<filename>', endpoint='audio')
def audio(filename):
    # print('temp/' + str('filename'))
    # file_path = os.path.join('temp', filename)
    # if os.path.exists(file_path):
    #     print(f"Serving file: {file_path}")
    return send_from_directory('temp', filename)
    # else:
    #     print(f"File not found: {file_path}")
    #     return "File not found", 404

@app.route('/api/get_text')
def get_text():
    # Example Python method returning data
    with open("temp/myFile.txt", "r", encoding='utf-8') as question:
        text = question.read().split("\n")
    with open("temp/syncmap.json", "r", encoding='utf-8') as interval:
        data = json.load(interval)
        intervals = [float(fragment["begin"]) for fragment in data["fragments"]]
    response = [[intervals[i], text[i]] for i in range(len(intervals))]
    return jsonify(response)

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
    with open("temp/answer.txt", "r", encoding='utf-8') as answer:
        return answer.read()

if __name__ == '__main__':
    app.run(debug=True)
    # from waitress import serve
    # serve(app, host="0.0.0.0", port=5000)