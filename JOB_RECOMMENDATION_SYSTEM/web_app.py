#!/usr/bin/env python3
"""
Job Recommendation System - Web Interface

A Flask-based web app for uploading resumes and viewing job recommendations.

Usage:
    pip install flask
    python web_app.py

Then open http://127.0.0.1:5000 in your browser.
"""

import os
import sys
from flask import Flask, render_template, request, jsonify, flash
from werkzeug.utils import secure_filename
import json

# Import our modules
from resume_parser import ResumeParser
from recommendation_engine import JobRecommendationEngine

app = Flask(__name__)
app.secret_key = 'job-recommendation-secret-key'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize components
resume_parser = ResumeParser()
job_engine = JobRecommendationEngine()


def allowed_file(filename):
    """Check if file has allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_resume():
    """Handle resume upload and return recommendations."""
    if 'resume' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['resume']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Only PDF files are allowed'}), 400

    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Get parameters
        top_n = request.form.get('top_n', 5, type=int)
        min_match = request.form.get('min_match', 20, type=float)

        # Parse resume
        resume_data = resume_parser.parse_resume(filepath)

        # Get recommendations
        recommendations = job_engine.get_recommendations(
            resume_data,
            top_n=top_n,
            min_skill_match=min_match
        )

        # Clean up uploaded file
        os.remove(filepath)

        # Prepare response
        return jsonify({
            'success': True,
            'resume': {
                'filename': resume_data['file_name'],
                'skills': resume_data['skills'],
                'skill_count': resume_data['skill_count'],
                'experience_level': resume_data['experience_level']
            },
            'recommendations': recommendations,
            'total_jobs': len(job_engine.jobs)
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/jobs')
def get_jobs():
    """API endpoint to get all jobs."""
    return jsonify({
        'jobs': job_engine.jobs,
        'total': len(job_engine.jobs)
    })


@app.route('/api/skills')
def get_skills():
    """API endpoint to get all unique skills from job database."""
    return jsonify({
        'skills': sorted(list(job_engine.get_all_skills())),
        'total': len(job_engine.get_all_skills())
    })


if __name__ == '__main__':
    print("=" * 60)
    print("  Job Recommendation System - Web Interface")
    print("=" * 60)
    print("\nStarting Flask server...")
    print("Open your browser to: http://127.0.0.1:5000\n")
    app.run(debug=True, host='127.0.0.1', port=5000)
