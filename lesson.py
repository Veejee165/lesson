from flask import Flask, render_template, request
import openai
import re

app = Flask(__name__)

# Configure OpenAI API credentials
openai.api_key = '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'

def extract_text_by_heading(lesson_text, heading):
    start_index = lesson_text.find(heading)
    if start_index != -1:
        start_index = lesson_text.find("\n", start_index) + 1  # Find the start of the content
        end_index = lesson_text.find("\n\n", start_index)  # Find the end of the content
        if end_index != -1:
            return lesson_text[start_index:end_index].strip()  # Extract the text and remove leading/trailing whitespace
        else:
            return lesson_text[start_index:].strip()  # If end index not found, extract until the end of the text
    else:
        return None  # Return None if the heading is not found

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
    chatgpt_prompt = f"Subject: {subject}\nClass Level: {class_level}\nLearning Objectives: {learning_objectives}\nDuration: {duration}\nTeacher Name: {teacher_name}\n\nMain Topics:\n1. Supporting material\n2. Key Vocabulary\n3. Knowledge: This refers to what the teacher wants the students to learn. It includes a list of key areas of knowledge\n4. Skills: Skills they want students to be proficient in: This includes topic-specific skills that are being developed and taken from the curriculum.\n5.Differentiation (Med): This component encourages the teacher to think about how they will make the lesson different for students who may have different learning needs.  \n6.Learning experiences (Med): This component is divided into sixsections that describe the different stages of the lesson: prepare, plan, investigate, apply, connect, and evaluate and reflect.\na) Prepare: This section of the lesson plan is focused on preparing the students for the topic that will be covered. Educators can use this time to introduce the topic, ask general questions to assess the students' prior knowledge, and engage the students with activities that will spark their interest in the topic.\nb)Plan: In the planning section, educators will lay out the activities that they will do with the students during the lesson. This will give the students a clear understanding of what to expect, and help the educator to structure the lesson in a logical way. If it's a longer lesson, the educator might break the activities down into sections to help students stay engaged and focused.\nc)Investigate: During this part of the lesson, the students will be actively engaged in the topic. This might involve watching a video, conducting an experiment, or participating in a group discussion.\nd)Apply: Once the investigation is complete, the students will use the knowledge they have gained to create something. This might involve creating a poster, a presentation, or a written report.\ne)Connect: In this section, educators will help the students make connections between the topic they are studying and the world around them. This might involve discussing current events or exploring how the topic relates to different cultures or regions.\nf)Evaluate and reflect: Finally, students willreflect on what they have learned. This might include thinking about what they enjoyed, what new skills and knowledge they gained, and what they could have done better. \n7)Educator assessment: This component is focused on how the teacher will assess what the students have learned. This might involve quizzes, rubrics, or other forms of  summative end-of-lesson assessments. \n8)Educator reflection: This component encourages the teacher to reflect on the content of the lesson, whether it was at the right level, whether there were any issues, and whether the pacing was appropriate. It also encourages the teacher to reflect on whether there was enough differentiation for students with different learning needs. \n\nGenerate a indepth lesson plan with sections with headings as the main topics listed above.Dont number or put anything before the headings just put the text in a new line whenever there is a heading\n"

    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=chatgpt_prompt,
        max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.7
    )

    # Extract the generated lesson plan from ChatGPT response
    lesson_text = response.choices[0].text.strip()
    print(lesson_text)
    print('')

    headings = ['Supporting Material','Key Vocabulary','Knowledge','Skills','Differentiation ','Prepare', 'Plan', 'Investigate', 'Apply', 'Connect', 'Evaluate and Reflect', 'Educator Assessment', 'Educator Reflection']
    extracted_text = {}
    for heading in headings:
        extracted_text[heading] = extract_text_by_heading(lesson_text, heading)
    extracted_text['subject']=subject
    extracted_text['classlev']=class_level
    extracted_text['learn']=learning_objectives
    extracted_text['dura']=duration
    extracted_text['tname']=teacher_name


    return render_template('lesson_plan.html', extracted_text=extracted_text)



if __name__ == '__main__':
    app.run(debug=True)

