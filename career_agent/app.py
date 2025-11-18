from flask import Flask, render_template, request, redirect, url_for
from resume_parser import parse_resume, match_experience_to_job
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_resume():
    name = request.form.get('name')
    contact = request.form.get('contact')
    if 'resume' not in request.files:
        return 'No file part', 400
    file = request.files['resume']
    if file.filename == '':
        return 'No selected file', 400
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(filepath)
        data = parse_resume(filepath)
        # Display extracted data and user info
        return render_template('display_resume.html', name=name, contact=contact, data=data)
    return 'Upload failed', 400

@app.route('/check_job', methods=['POST'])
def check_job():
    job_desc = request.form.get('job_description')
    resume_path = request.form.get('resume_path')
    data = parse_resume(resume_path)
    feedback = match_experience_to_job(data, job_desc)
    return render_template('result.html', data=data, job_desc=job_desc, feedback=feedback)

@app.route('/ask_roles', methods=['POST'])
def ask_roles():
    job_desc = request.form.get('job_description')
    # Placeholder: In a real app, fetch roles/responsibilities from a database or API
    roles = f"Roles and responsibilities for the job: {job_desc}\n- Example Role 1\n- Example Role 2\n- Example Responsibility 1\n- Example Responsibility 2"
    return render_template('roles.html', job_desc=job_desc, roles=roles)

if __name__ == '__main__':
    app.run(debug=True)
