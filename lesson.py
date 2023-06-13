from flask import Flask, render_template, request
import openai

app = Flask(__name__)

# Configure OpenAI API credentials
openai.api_key = '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'
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_lesson_plan', methods=['POST'])
def generate_lesson_plan():
    # Retrieve form inputs
    subject = request.form['subject']
    class_level = request.form['class_level']
    learning_objectives = request.form['learning_objectives']
    duration = request.form['duration']
    teacher_name = request.form['teacher_name']

    # Generate additional sections with ChatGPT
    chatgpt_prompt = f"Subject: {subject}\nClass Level: {class_level}\nLearning Objectives: {learning_objectives}\nDuration: {duration}\nTeacher Name: {teacher_name}\nGenerate Lesson Plan:"
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=chatgpt_prompt,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.7
    )

    # Extract the generated lesson plan from ChatGPT response
    generated_plan = response.choices[0].text.strip()

    # Render the lesson_plan.html template with form inputs and generated plan
    return render_template('lesson_plan.html',
                           subject=subject,
                           class_level=class_level,
                           learning_objectives=learning_objectives,
                           duration=duration,
                           teacher_name=teacher_name,
                           generated_plan=generated_plan)


if __name__ == '__main__':
    app.run(debug=True)
