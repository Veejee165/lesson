from flask import Flask, render_template, request
import openai

app = Flask(__name__)

# Configure OpenAI API credentials
openai.api_key = "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"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_lesson_plan', methods=['POST'])
def generate_lesson_plan():
    # Retrieve user inputs from the form
    subject = request.form['subject']
    class_level = request.form['class_level']
    learning_objectives = request.form['learning_objectives']
    duration = request.form['duration']

    # Generate the prompt for the lesson plan
    prompt = f"Subject: {subject}\nClass Level: {class_level}\nLearning Objectives: {learning_objectives}\nDuration: {duration}\nGenerate a lesson plan:"

    try:
        # Send request to OpenAI API
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=prompt,
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.7
        )

        # Extract the generated lesson plan from the API response
        lesson_plan = response.choices[0].text.strip()

        return render_template('lesson_plan.html', lesson_plan=lesson_plan)
    except Exception as e:
        # Handle API errors
        error_message = f"An error occurred: {str(e)}"
        return render_template('error.html', error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
