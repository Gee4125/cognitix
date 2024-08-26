from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template_string,render_template, request, redirect, url_for, session , jsonify
import os
import speech_recognition as sr
from pydub import AudioSegment
import io
import secrets

def generate_secret_key():
    return secrets.token_hex(16)

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = generate_secret_key()

# Empathy scores for different options
empathy_scores = {
    'form_page_1': {'A': 1, 'B': 10, 'C': 5, 'D': 8},
    'form_page_2': {'A': 6, 'B': 10, 'C': 4, 'D': 1},
    'form_page_3': {'A': 2, 'B': 10, 'C': 3, 'D': 2},
    'form_page_4': {'A': 5, 'B': 8, 'C': 3, 'D': 1},
    'form_page_5': {'A': 7, 'B': 9, 'C': 4, 'D': 2}
}

# Evaluation metrics
# Evaluation metrics with more detailed categories
def evaluate_empathy(score):
    if score >= 31:
        return "Very High Empathy: You demonstrate an exceptional ability to understand and connect with others' emotions. Your empathy is deeply ingrained in your interactions and responses."
    elif score >= 26:
        return "High Empathy: You have a strong sense of empathy and are very attuned to the emotions and needs of others. You consistently show compassion and understanding."
    elif score >= 21:
        return "Moderate Empathy: You have a good level of empathy and usually respond well to others' emotions. You may occasionally miss some subtle cues but generally show understanding."
    elif score >= 16:
        return "Average Empathy: Your empathy is average. You are aware of others' feelings but may not always fully grasp their emotions or react as sensitively as possible."
    elif score >= 11:
        return "Low Empathy: You might find it challenging to understand and relate to others' feelings. There may be room for improvement in recognizing and responding to emotional cues."
    else:
        return "Very Low Empathy: You have significant difficulty in understanding and relating to others' emotions. Developing greater emotional awareness and sensitivity could benefit your relationships."

# Set the paths to the static files
image_path = 'C:\Dharsh\projects\full stack\proj_1\static\background-image.png'
audio_path = 'C:\Dharsh\projects\full stack\proj_1\static\audio-file.mp3'
bg_image_path = 'C:\Dharsh\projects\full stack\proj_1\static\background.png'
image1_path = 'C:\Dharsh\projects\full stack\proj_1\static\1_k.jpeg'
image2_path = 'C:\Dharsh\projects\full stack\proj_1\static\2_k.jpeg'
audio_path = 'C:\Dharsh\projects\full stack\proj_1\static\audio.mp3'

# Empathy scores for different options
adaptability_scores = {
    'scenario_1': {'A': 2, 'B': 8, 'C': 5, 'D': 3},
    'scenario_2': {'A': 2, 'B': 8, 'C': 5, 'D': 3},
    'scenario_3': {'A': 2, 'B': 8, 'C': 5, 'D': 6},
    'scenario_4': {'A': 2, 'B': 8, 'C': 5, 'D': 3},
    'scenario_5': {'A': 2, 'B': 8, 'C': 3, 'D': 5}
}


# Evaluation metrics
def evaluate_adaptability(score):
    if score >= 35:
        return "Highly Adaptable - You excel in adapting to new situations and changes. You are flexible, resilient, and thrive in dynamic environments."
    elif score >= 25:
        return "Moderately Adaptable - You are fairly adaptable and can handle changes well, though there may be times when you find adjustments challenging."
    elif score >= 15:
        return "Average Adaptability - Your adaptability is average. You manage changes adequately but may feel uncomfortable with significant or sudden shifts."
    elif score >= 5:
        return "Low Adaptability - You might find it challenging to adapt to new situations and changes. Working on being more open to new experiences could help improve your adaptability."
    else:
        return "You struggle significantly with adapting to change. Developing greater flexibility and resilience can help you navigate changes more effectively."



# Initialize the recognizer
recognizer = sr.Recognizer()

# Texts for the user to read
expected_text1 = "The quick brown fox jumps over the lazy dog"
expected_text2 = "Pack my box with five dozen liquor jugs"

@app.route('/')
def main_page():
    return render_template('MAIN_PAGE_HTML.html')

@app.route('/login_page')
def login_page():
    return render_template('LOGIN_SIGNUP_HTML.html')

@app.route('/login', methods=['POST'])
def login():
    gmail_id = request.form['gmail-id']
    password = request.form['password']
    # Add your login logic here
    return redirect(url_for('topics_page'))

@app.route('/signup', methods=['POST'])
def signup():
    first_name = request.form['first-name']
    last_name = request.form['last-name']
    gmail_id = request.form['gmail-id']
    phone = request.form['phone']
    dob = request.form['dob']
    gender = request.form['gender']
    address = request.form['address']
    password = request.form['password']
    # Add your signup logic here
    return redirect(url_for('topics'))

@app.route('/topics')
def topics_page():
    return render_template('TOPICS_PAGE_HTML.html')

@app.route('/topics/<topic_name>')
def topic_page(topic_name):
    # Placeholder logic for topic page content
    return f"This is the page for {topic_name.capitalize()}."

@app.route("/index")
def index_f():
    return render_template('FIRST_PAGE.html')

@app.route('/form_page_1', methods=['GET', 'POST'])
def form_page_1():
    if request.method == 'POST':
        selected_option = request.form.get('response')
        score = empathy_scores['form_page_1'].get(selected_option, 0)
        session['total_score'] = score
        return redirect(url_for('second_page'))
    return render_template('form_html1.html')

@app.route('/second_page')
def second_page():
    return render_template('second_html.html')

@app.route('/form_page_2', methods=['GET', 'POST'])
def form_page_2():
    if request.method == 'POST':
        selected_option = request.form.get('response')
        score = empathy_scores['form_page_2'].get(selected_option, 0)
        session['total_score'] += score
        return redirect(url_for('third_page'))
    return render_template('form_html2.html')

@app.route('/third_page')
def third_page():
    return render_template('third_html.html')

@app.route('/form_page_3', methods=['GET', 'POST'])
def form_page_3():
    if request.method == 'POST':
        selected_option = request.form.get('response')
        score = empathy_scores['form_page_3'].get(selected_option, 0)
        session['total_score'] += score
        return redirect(url_for('fourth_page'))
    return render_template('form_html3.html')

@app.route('/fourth_page')
def fourth_page():
    return render_template('fourth_html.html')

@app.route('/form_page_4', methods=['GET', 'POST'])
def form_page_4():
    if request.method == 'POST':
        selected_option = request.form.get('response')
        score = empathy_scores['form_page_4'].get(selected_option, 0)
        session['total_score'] += score
        return redirect(url_for('fifth_page'))
    return render_template('form_html4.html')

@app.route('/fifth_page')
def fifth_page():
    return render_template('five_html.html')

@app.route('/form_page_5', methods=['GET', 'POST'])
def form_page_5():
    if request.method == 'POST':
        selected_option = request.form.get('response')
        score = empathy_scores['form_page_5'].get(selected_option, 0)
        session['total_score'] += score
        return redirect(url_for('result_page'))
    return render_template('form_html5.html')
@app.route('/result_page')
def result_page():
    total_score = session.get('total_score', 0)
    result_text = evaluate_empathy(total_score)
    return render_template('result_html_template.html', total_score=total_score, result_text=result_text)
# Routes for pages - adaptability
@app.route('/starting')
def starting_page():
    return render_template('FIRST_PAGE_A.html')

@app.route('/form_page_1_a', methods=['GET', 'POST'])
def form_page_1_a():
    if request.method == 'POST':
        session['response_1'] = request.form['response']
        return redirect(url_for('second_page_a'))
    return render_template('form_html1_a.html')

@app.route('/second_page_a')
def second_page_a():
    return render_template('second_html_a.html')

@app.route('/form_page_2_a', methods=['GET', 'POST'])
def form_page_2_a():
    if request.method == 'POST':
        session['response_2'] = request.form['response']
        return redirect(url_for('third_page_a'))
    return render_template('form_html2_a.html')

@app.route('/third_page_a')
def third_page_a():
    return render_template('third_html_a.html')

@app.route('/form_page_3_a', methods=['GET', 'POST'])
def form_page_3_a():
    if request.method == 'POST':
        session['response_3'] = request.form['response']
        return redirect(url_for('fourth_page_a'))
    return render_template('form_html3_a.html')

@app.route('/fourth_page_a')
def fourth_page_a():
    return render_template('fourth_html_a.html')

@app.route('/form_page_4_a', methods=['GET', 'POST'])
def form_page_4_a():
    if request.method == 'POST':
        session['response_4'] = request.form['response']
        return redirect(url_for('fifth_page_a'))
    return render_template('form_html4_a.html')

@app.route('/fifth_page_a')
def fifth_page_a():
    return render_template('fifth_html_a.html')

@app.route('/form_page_5_a', methods=['GET', 'POST'])
def form_page_5_a():
    if request.method == 'POST':
        session['response_5'] = request.form['response']
        return redirect(url_for('results_a'))
    return render_template('form_html5_a.html')

@app.route('/results_a')
def results_a():
    responses = [
        session.get('response_1'),
        session.get('response_2'),
        session.get('response_3'),
        session.get('response_4'),
        session.get('response_5')
    ]

    total_score = sum(
        adaptability_scores[f'scenario_{i+1}'].get(response, 0)
        for i, response in enumerate(responses)
    )

    adaptability_rating = evaluate_adaptability(total_score)

    return render_template('result_html_a.html', adaptability_score=total_score, adaptability_rating=adaptability_rating)
@app.route('/logic_first')
def Logic_first():
    return render_template('sudoku_html.html')

@app.route('/memory_game')
def memory_game():
    return render_template('memory_html.html')

# @app.route('/static/style.css')
# def serve_css():
#     return sudoku_css, 200, {'Content-Type': 'text/css'}

# @app.route('/static/script.js')
# def serve_js():
#     return sudoku_js, 200, {'Content-Type': 'application/javascript'}

# @app.route('/static/memory_style.css')
# def serve_memory_css():
#     return memory_css, 200, {'Content-Type': 'text/css'}

# @app.route('/static/memory_script.js')
# def serve_memory_js():
#     return memory_js, 200, {'Content-Type': 'application/javascript'}
@app.route('/sudoku_css')
def serve_css():
    return render_template('sudoku_css.css')

@app.route('/sudoku_js')
def serve_js():
    return render_template('sudoku_js.js')

@app.route('/memory_style')
def serve_memory_css():
    return render_template('memory_css.css')

@app.route('/memory_script')
def serve_memory_js():
    return render_template('memory_js.js')



@app.route('/page1')
def page1():
    return render_template('page1_html_s.html')

@app.route('/speech-recognition')
def index():
    return render_template('index_html_s.html', expected_text1=expected_text1, expected_text2=expected_text2)

# @app.route('/record', methods=['POST'])
# def record():
#     audio_file = request.files['audio']

#     # Convert the audio file to WAV format
#     audio = AudioSegment.from_file(audio_file)
#     audio_wav = io.BytesIO()
#     audio.export(audio_wav, format="wav")
#     audio_wav.seek(0)

#     # Save the WAV file temporarily to check it
#     with open("/tmp/test.wav", "wb") as f:
#         f.write(audio_wav.getvalue())

#     # Recognize speech using speech_recognition
#     try:
#         with sr.AudioFile(audio_wav) as source:
#             audio_data = recognizer.record(source)
#             recognized_text = recognizer.recognize_google(audio_data)
#             print(f"You said: {recognized_text}")

#             # Compare the recognized speech with the expected text
#             accuracy1 = calculate_accuracy(recognized_text, expected_text1)
#             accuracy2 = calculate_accuracy(recognized_text, expected_text2)

#             return render_template('result_html.html', recognized_text=recognized_text, accuracy1=accuracy1, accuracy2=accuracy2)
#     except sr.UnknownValueError:
#         return "Google Speech Recognition could not understand audio"
#     except sr.RequestError as e:
#         return f"Could not request results from Google Speech Recognition service; {e}"

@app.route('/record', methods=['POST'])
def record():
    audio_file = request.files['audio']

    # Convert the audio file to WAV format
    audio = AudioSegment.from_file(audio_file, format="webm")
    audio_wav = io.BytesIO()
    audio.export(audio_wav, format="wav")
    audio_wav.seek(0)

    # Save the WAV file temporarily to check it
    with open("/tmp/test.wav", "wb") as f:
        f.write(audio_wav.getvalue())

    # Recognize speech using speech_recognition
    try:
        with sr.AudioFile(audio_wav) as source:
            audio_data = recognizer.record(source)
            recognized_text = recognizer.recognize_google(audio_data, language="en-US")
            print(f"You said: {recognized_text}")

            # Compare the recognized speech with the expected text
            accuracy1 = calculate_accuracy(recognized_text, expected_text1)
            accuracy2 = calculate_accuracy(recognized_text, expected_text2)

            return render_template('result_html.html', recognized_text=recognized_text, accuracy1=accuracy1, accuracy2=accuracy2)
    except sr.UnknownValueError:
        return "Google Speech Recognition could not understand audio"
    except sr.RequestError as e:
        return f"Could not request results from Google Speech Recognition service; {e}"

def calculate_accuracy(recognized_text, expected_text):
    recognized_words = recognized_text.lower().split()
    expected_words = expected_text.lower().split()
    matching_words = sum(1 for i, word in enumerate(recognized_words) if i < len(expected_words) and word == expected_words[i])
    accuracy = matching_words / len(expected_words) * 100
    return accuracy

@app.route('/result')
def result():
    # Process the results and render the result page
    result_text1 = 'Thank you!!!'  # Process text 1 result here
    result_text2 = 'Please move to the next section - that is listening'  # Process text 2 result here
    return render_template('result_html.html', result_text1=result_text1, result_text2=result_text2)

@app.route('/next')
def next_page():
    return render_template('page1_html.html')

@app.route('/page2')
def page2():
    return render_template('page2_html.html')

@app.route('/submit_answers', methods=['POST'])
def submit_answers():
    user_answers = request.json['answers']
    correct_answers = [
        "c",  # the string
        "d",  # soar high
        "b",  # follow a set of rules
        "a",  # track
        "b",  # chaos
        "c"   # the importance of discipline
    ]
    score = sum(1 for user, correct in zip(user_answers, correct_answers) if user.lower() == correct)
    return jsonify({'score': score, 'total': len(correct_answers)})
@app.route('/final_page')
def final_page():
    return render_template('FINAL_PAGE_HTML.html')

if __name__ == "__main__":
    app.run()