#!/usr/bin/env python3
"""
Sample Resume Generator

This script creates sample PDF resumes for testing the job recommendation system.
Requires: reportlab (pip install reportlab)
"""

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import os


def create_sample_resume(filename, name, title, experience, skills, education, projects=None):
    """
    Create a sample resume PDF.

    Args:
        filename (str): Output filename
        name (str): Candidate name
        title (str): Job title
        experience (list): List of experience dicts
        skills (list): List of skills
        education (list): List of education entries
        projects (list): Optional list of projects
    """
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )

    styles = getSampleStyleSheet()
    elements = []

    # Name
    name_style = ParagraphStyle(
        'Name',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=6,
        alignment=1  # Center
    )
    elements.append(Paragraph(name, name_style))

    # Title
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.gray,
        spaceAfter=12,
        alignment=1
    )
    elements.append(Paragraph(title, title_style))

    # Contact info placeholder
    contact_style = ParagraphStyle(
        'Contact',
        parent=styles['Normal'],
        fontSize=10,
        alignment=1
    )
    elements.append(Paragraph("email@example.com | (555) 123-4567 | LinkedIn: /in/username | GitHub: github.com/username", contact_style))
    elements.append(Spacer(1, 0.2*inch))

    # Summary
    elements.append(Paragraph("PROFESSIONAL SUMMARY", styles['Heading3']))
    elements.append(Spacer(1, 0.1*inch))
    summary = f"Results-driven {title.lower()} with {len(experience)} years of experience. " \
              f"Skilled in {', '.join(skills[:5])} and passionate about building scalable solutions."
    elements.append(Paragraph(summary, styles['Normal']))
    elements.append(Spacer(1, 0.2*inch))

    # Skills
    elements.append(Paragraph("TECHNICAL SKILLS", styles['Heading3']))
    elements.append(Spacer(1, 0.1*inch))
    skills_text = " • ".join(skills)
    elements.append(Paragraph(skills_text, styles['Normal']))
    elements.append(Spacer(1, 0.2*inch))

    # Experience
    elements.append(Paragraph("PROFESSIONAL EXPERIENCE", styles['Heading3']))
    elements.append(Spacer(1, 0.1*inch))

    for exp in experience:
        elements.append(Paragraph(f"<b>{exp['title']}</b> | {exp['company']} | {exp['dates']}", styles['Normal']))
        elements.append(Spacer(1, 0.05*inch))
        for bullet in exp['bullets']:
            elements.append(Paragraph(f"• {bullet}", styles['Normal']))
        elements.append(Spacer(1, 0.1*inch))

    # Education
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph("EDUCATION", styles['Heading3']))
    elements.append(Spacer(1, 0.1*inch))
    for edu in education:
        elements.append(Paragraph(f"<b>{edu['degree']}</b> - {edu['school']}, {edu['year']}", styles['Normal']))
    elements.append(Spacer(1, 0.1*inch))

    # Projects (optional)
    if projects:
        elements.append(Paragraph("PROJECTS", styles['Heading3']))
        elements.append(Spacer(1, 0.1*inch))
        for proj in projects:
            elements.append(Paragraph(f"<b>{proj['name']}</b>: {proj['description']}", styles['Normal']))
        elements.append(Spacer(1, 0.1*inch))

    doc.build(elements)
    print(f"✓ Created: {filename}")


def main():
    """Generate sample resumes for testing."""
    output_dir = "sample_resumes"
    os.makedirs(output_dir, exist_ok=True)

    # Resume 1: Python Developer
    create_sample_resume(
        f"{output_dir}/python_developer_resume.pdf",
        "John Smith",
        "Senior Python Software Engineer",
        [
            {
                "title": "Senior Python Developer",
                "company": "TechCorp Inc",
                "dates": "2020 - Present",
                "bullets": [
                    "Developed scalable web applications using Django and Flask",
                    "Implemented REST APIs serving 1M+ requests daily",
                    "Optimized PostgreSQL queries reducing latency by 40%",
                    "Led team of 5 developers in Agile environment"
                ]
            },
            {
                "title": "Software Engineer",
                "company": "StartupXYZ",
                "dates": "2018 - 2020",
                "bullets": [
                    "Built microservices using Python and Docker",
                    "Implemented CI/CD pipelines with Jenkins",
                    "Collaborated with frontend team using React"
                ]
            }
        ],
        ["Python", "Django", "Flask", "PostgreSQL", "Docker", "AWS", "Git", "REST API", "Microservices", "Redis", "Celery", "pytest"],
        [{"degree": "B.S. Computer Science", "school": "University of Technology", "year": "2018"}],
        [
            {"name": "E-Commerce Platform", "description": "Full-stack Django application with payment integration"},
            {"name": "Data Pipeline", "description": "Automated ETL pipeline processing 10GB+ daily"}
        ]
    )

    # Resume 2: Data Scientist
    create_sample_resume(
        f"{output_dir}/data_scientist_resume.pdf",
        "Sarah Johnson",
        "Machine Learning Engineer",
        [
            {
                "title": "Machine Learning Engineer",
                "company": "AI Innovations",
                "dates": "2021 - Present",
                "bullets": [
                    "Built NLP models using transformers and BERT",
                    "Developed recommendation systems with TensorFlow",
                    "Deployed models to production using Docker and Kubernetes",
                    "Reduced inference time by 60% through optimization"
                ]
            },
            {
                "title": "Data Scientist",
                "company": "DataCorp Analytics",
                "dates": "2019 - 2021",
                "bullets": [
                    "Analyzed large datasets using Pandas and NumPy",
                    "Built predictive models with scikit-learn",
                    "Created dashboards using Tableau and Matplotlib",
                    "Presented insights to stakeholders weekly"
                ]
            }
        ],
        ["Python", "Machine Learning", "TensorFlow", "PyTorch", "NLP", "Pandas", "NumPy", "scikit-learn", "Deep Learning", "SQL", "AWS", "Docker", "Jupyter", "Statistics"],
        [{"degree": "M.S. Data Science", "school": "Stanford University", "year": "2019"},
         {"degree": "B.S. Mathematics", "school": "UC Berkeley", "year": "2017"}]
    )

    # Resume 3: Frontend Developer
    create_sample_resume(
        f"{output_dir}/frontend_developer_resume.pdf",
        "Mike Chen",
        "Frontend Developer",
        [
            {
                "title": "Frontend Developer",
                "company": "Creative Agency",
                "dates": "2021 - Present",
                "bullets": [
                    "Built responsive web applications with React",
                    "Implemented state management using Redux",
                    "Created reusable component library in TypeScript",
                    "Optimized performance achieving 95+ Lighthouse scores"
                ]
            },
            {
                "title": "Junior Web Developer",
                "company": "Digital Solutions",
                "dates": "2020 - 2021",
                "bullets": [
                    "Developed websites using HTML, CSS, JavaScript",
                    "Collaborated with designers using Figma",
                    "Implemented responsive designs with Tailwind CSS"
                ]
            }
        ],
        ["JavaScript", "React", "TypeScript", "HTML", "CSS", "Tailwind", "Redux", "Node.js", "Git", "Webpack", "Jest", "Figma"],
        [{"degree": "B.A. Web Design", "school": "Design Institute", "year": "2020"}]
    )

    # Resume 4: DevOps Engineer
    create_sample_resume(
        f"{output_dir}/devops_engineer_resume.pdf",
        "Alex Rivera",
        "DevOps Engineer",
        [
            {
                "title": "Senior DevOps Engineer",
                "company": "CloudFirst Tech",
                "dates": "2019 - Present",
                "bullets": [
                    "Managed Kubernetes clusters with 100+ nodes",
                    "Implemented Infrastructure as Code using Terraform",
                    "Set up CI/CD pipelines with Jenkins and GitHub Actions",
                    "Reduced deployment time by 70% through automation"
                ]
            },
            {
                "title": "Systems Administrator",
                "company": "Enterprise Systems",
                "dates": "2016 - 2019",
                "bullets": [
                    "Administered Linux servers (Ubuntu, CentOS)",
                    "Implemented monitoring with Prometheus and Grafana",
                    "Automated tasks using Python and Bash scripting"
                ]
            }
        ],
        ["Docker", "Kubernetes", "AWS", "Terraform", "Python", "Linux", "Jenkins", "CI/CD", "Ansible", "Prometheus", "Grafana", "Bash", "Git", "Security"],
        [{"degree": "B.S. Information Technology", "school": "State University", "year": "2016"}]
    )

    print(f"\n✓ Generated 4 sample resumes in '{output_dir}/'")
    print("\nTest the recommendation system with:")
    print(f"  python main.py --resume {output_dir}/python_developer_resume.pdf --detailed")
    print(f"  python main.py --resume {output_dir}/data_scientist_resume.pdf --detailed")
    print(f"  python main.py --resume {output_dir}/frontend_developer_resume.pdf --detailed")
    print(f"  python main.py --resume {output_dir}/devops_engineer_resume.pdf --detailed")


if __name__ == '__main__':
    try:
        from reportlab.lib import colors
    except ImportError:
        print("Error: reportlab is required to generate sample resumes.")
        print("Install it with: pip install reportlab")
        exit(1)

    main()
