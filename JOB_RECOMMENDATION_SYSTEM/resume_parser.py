"""
Resume Parser Module - Extracts text and skills from PDF resumes
"""

import PyPDF2
import re
import os


class ResumeParser:
    """Parse PDF resumes and extract relevant information."""

    def __init__(self):
        # Common technical skills to look for
        self.skill_keywords = {
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust',
            'ruby', 'php', 'swift', 'kotlin', 'scala', 'r', 'matlab', 'dart',
            'html', 'css', 'sql', 'bash', 'powershell', 'perl',
            'react', 'angular', 'vue', 'svelte', 'next.js', 'nuxt.js', 'gatsby',
            'node.js', 'express', 'django', 'flask', 'fastapi', 'spring boot', 'rails',
            'mongodb', 'postgresql', 'mysql', 'sqlite', 'oracle', 'dynamodb', 'cassandra',
            'redis', 'elasticsearch', 'firebase', 'supabase',
            'aws', 'azure', 'gcp', 'google cloud', 'heroku', 'netlify', 'vercel',
            'docker', 'kubernetes', 'terraform', 'ansible', 'jenkins', 'github actions',
            'git', 'gitlab', 'bitbucket', 'svn',
            'machine learning', 'deep learning', 'nlp', 'computer vision', 'ai',
            'tensorflow', 'pytorch', 'scikit-learn', 'keras', 'xgboost', 'lightgbm',
            'pandas', 'numpy', 'scipy', 'matplotlib', 'seaborn', 'plotly', 'tableau',
            'power bi', 'looker', 'jupyter', 'rstudio',
            'hadoop', 'spark', 'kafka', 'airflow', 'dbt', 'snowflake', 'bigquery',
            'rest api', 'graphql', 'grpc', 'websockets', 'soap', 'microservices',
            'linux', 'unix', 'windows', 'macos', 'ubuntu', 'centos', 'debian',
            'ci/cd', 'devops', 'agile', 'scrum', 'kanban', 'jira', 'confluence',
            'blockchain', 'smart contracts', 'solidity', 'web3',
            'selenium', 'cypress', 'jest', 'mocha', 'junit', 'pytest', 'cucumber',
            'android', 'ios', 'flutter', 'react native', 'xamarin', 'ionic',
            'tailwind', 'bootstrap', 'sass', 'less', 'styled-components', 'material ui',
            'figma', 'sketch', 'adobe xd', 'photoshop', 'illustrator',
            'prometheus', 'grafana', 'datadog', 'new relic', 'splunk',
            'oauth', 'jwt', 'ssl', 'cybersecurity', 'penetration testing', 'siem'
        }

    def extract_text_from_pdf(self, pdf_path):
        """
        Extract text from a PDF file.

        Args:
            pdf_path (str): Path to the PDF file

        Returns:
            str: Extracted text content
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")

        return text

    def clean_text(self, text):
        """
        Clean and normalize extracted text.

        Args:
            text (str): Raw extracted text

        Returns:
            str: Cleaned text
        """
        # Remove special characters and normalize whitespace
        text = re.sub(r'[^\w\s\-\+\.\/\@]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.lower().strip()

    def extract_skills(self, text):
        """
        Extract skills from resume text.

        Args:
            text (str): Resume text

        Returns:
            set: Set of found skills
        """
        text_clean = self.clean_text(text)
        text_words = set(text_clean.split())

        found_skills = set()

        # Check for multi-word skills first
        text_lower = text.lower()
        for skill in self.skill_keywords:
            if ' ' in skill:  # Multi-word skills
                if skill in text_lower or skill.replace(' ', '') in text_lower:
                    found_skills.add(skill)
            else:
                # Check whole words for single-word skills
                if skill in text_words:
                    found_skills.add(skill)

        return found_skills

    def parse_resume(self, pdf_path):
        """
        Parse a resume PDF and return structured data.

        Args:
            pdf_path (str): Path to the PDF file

        Returns:
            dict: Parsed resume data including text and skills
        """
        raw_text = self.extract_text_from_pdf(pdf_path)
        cleaned_text = self.clean_text(raw_text)
        skills = self.extract_skills(raw_text)

        # Try to extract experience level based on keywords
        experience_level = self._detect_experience_level(cleaned_text)

        return {
            'file_name': os.path.basename(pdf_path),
            'raw_text': raw_text,
            'cleaned_text': cleaned_text,
            'skills': sorted(list(skills)),
            'skill_count': len(skills),
            'experience_level': experience_level
        }

    def _detect_experience_level(self, text):
        """
        Detect experience level from resume text.

        Args:
            text (str): Cleaned resume text

        Returns:
            str: Detected experience level
        """
        text_lower = text.lower()

        # Count years of experience mentions
        patterns = [
            r'(\d+)\+?\s*years?\s*(of\s*)?experience',
            r'experience:\s*(\d+)\+?\s*years?',
            r'(\d+)\+?\s*years?\s*(in\s*)?(software|development|engineering)'
        ]

        years = 0
        for pattern in patterns:
            matches = re.findall(pattern, text_lower)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0]
                try:
                    years = max(years, int(match))
                except:
                    pass

        # Classify based on years
        if years >= 8:
            return 'Senior'
        elif years >= 3:
            return 'Mid-Level'
        elif years >= 0:
            return 'Junior'

        # Fallback to keyword detection
        if any(kw in text_lower for kw in ['senior', 'lead', 'principal', 'staff', 'architect', 'manager']):
            return 'Senior'
        elif any(kw in text_lower for kw in ['mid-level', 'mid level', 'intermediate', 'associate']):
            return 'Mid-Level'
        elif any(kw in text_lower for kw in ['junior', 'entry level', 'entry-level', 'fresh graduate', 'intern']):
            return 'Junior'

        return 'Unknown'


if __name__ == '__main__':
    # Test with a sample resume
    parser = ResumeParser()
    print("Resume Parser initialized successfully!")
    print(f"Total skills in database: {len(parser.skill_keywords)}")
