# 🎯 Job Recommendation System

A Python-based job recommendation system that analyzes PDF resumes and recommends matching job positions based on skills, experience, and content similarity.

## Features

- **PDF Resume Parsing**: Extracts text and identifies skills from PDF resumes
- **Intelligent Skill Matching**: Matches your skills against job requirements
- **TF-IDF Content Analysis**: Uses machine learning to analyze resume-job similarity
- **Experience Level Detection**: Automatically categorizes experience (Junior/Mid/Senior)
- **Customizable Filters**: Set minimum match thresholds and number of recommendations

## Project Structure

```
JOB_RECOMMENDATION_SYSTEM/
├── main.py                      # Main entry point
├── resume_parser.py             # PDF parsing and skill extraction
├── recommendation_engine.py     # Job matching and scoring logic
├── job_database.json            # Sample job listings database
├── requirements.txt             # Python dependencies
├── README.md                    # This file
└── sample_resumes/              # Sample resumes for testing
    └── (add your PDFs here)
```

## Installation

1. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
python main.py --resume path/to/your/resume.pdf
```

### Command Line Options

```bash
# Show top 10 recommendations
python main.py --resume resume.pdf --top 10

# Set minimum skill match percentage
python main.py --resume resume.pdf --min-match 50

# Show detailed information
python main.py --resume resume.pdf --detailed

# Combine options
python main.py --resume resume.pdf --top 10 --min-match 40 --detailed
```

### Interactive Mode

Run without arguments to use interactive mode:
```bash
python main.py
```

## How It Works

1. **Resume Parsing**
   - Extracts text from PDF using PyPDF2
   - Identifies skills from a predefined skill database
   - Detects experience level from keywords and years

2. **Job Matching**
   - Calculates TF-IDF cosine similarity between resume and job descriptions
   - Performs skill-by-skill matching
   - Evaluates experience level compatibility

3. **Scoring Algorithm**
   - Content Similarity: 40%
   - Skill Match: 40%
   - Experience Match: 20%

## Sample Output

```
======================================================================
  🎯 Job Recommendation System
======================================================================

--------------------------------------------------
  Step 1: Parsing Resume
--------------------------------------------------
✓ Successfully parsed resume: my_resume.pdf
  • Detected Experience Level: Mid-Level
  • Skills Found: 12

--------------------------------------------------
  Step 2: Loading Job Database
--------------------------------------------------
✓ Loaded 12 jobs from database

############################################################
  #1 | Python Software Engineer
############################################################
  Company:    Tech Solutions Inc
  Location:   San Francisco, CA (Remote)
  Salary:     $120,000 - $150,000
  Level:      Mid-Level

  ── Match Score: 87.5% ──
     • Content Similarity: 82.3%
     • Skill Match:        85.7% (6/7)
     • Experience Match:   100%

  ✅ Matched Skills: python, django, flask, postgresql, git, docker
  📋 Missing Skills: rest api
```

## Customizing the Job Database

Edit `job_database.json` to add or modify job listings:

```json
{
  "jobs": [
    {
      "id": 1,
      "title": "Your Job Title",
      "company": "Company Name",
      "location": "Location",
      "salary": "$X - $Y",
      "required_skills": ["skill1", "skill2", "skill3"],
      "description": "Job description here",
      "experience_level": "Mid-Level"
    }
  ]
}
```

## Adding New Skills

To add more skills to the parser, edit `resume_parser.py` and add to the `skill_keywords` set in the `__init__` method.

## Requirements

- Python 3.7+
- PyPDF2
- scikit-learn
- numpy
- pandas

## License

MIT License - feel free to use and modify!
