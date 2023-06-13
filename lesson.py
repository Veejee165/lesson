
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
    teacher_name = request.form['teacher_name']
    # key_vocabulary = request.form['key_vocabulary']
    # supporting_material = request.form['supporting_material']
    # learning_outcome = request.form['learning_outcome']
    # knowledge = request.form['knowledge']
    # skills = request.form['skills']
    # understanding = request.form['understanding']
    # differentiation = request.form['differentiation']

    # Generate the prompt for the lesson plan
    prompt = f"1. Lesson title (short): {subject}\n2. Teacher name (short): {teacher_name}\n3. Subject (short): {subject}\n4. Grade (short): {class_level}\n5. Date (short): \n6. Duration (short): {duration}\n7. Key vocabulary (short): \n8. Supporting material: \n9. Learning outcome (short): \n10. Knowledge: \n11. Skills: \n12. Understanding: \n13. Differentiation (Med): \n14. Learning experiences (Med):\n\nPrepare:\nPlan:\nInvestigate:\nApply:\nConnect:\nEvaluate and reflect:\n\nEducator assessment:\nEducator reflection:"

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
        return render_template('error.html', error_message=str(e))

if __name__ == '__main__':
    app.run(debug=True)
