"""
Job Recommendation Engine - Matches resumes to job postings
"""

import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


class JobRecommendationEngine:
    """Engine to recommend jobs based on resume content."""

    def __init__(self, jobs_database_path='job_database.json'):
        """
        Initialize the recommendation engine with job data.

        Args:
            jobs_database_path (str): Path to JSON file containing job listings
        """
        self.jobs = self._load_jobs(jobs_database_path)
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words='english',
            ngram_range=(1, 2),
            max_features=5000
        )
        self._prepare_job_vectors()

    def _load_jobs(self, filepath):
        """Load jobs from JSON file."""
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                return data.get('jobs', [])
        except FileNotFoundError:
            raise FileNotFoundError(f"Job database not found: {filepath}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON in job database: {filepath}")

    def _prepare_job_vectors(self):
        """Prepare TF-IDF vectors for all jobs."""
        self.job_texts = []
        for job in self.jobs:
            # Combine title, description, and skills for vectorization
            text = f"{job['title']} {job['description']} {' '.join(job['required_skills'])}"
            text = text.lower()
            self.job_texts.append(text)

        if self.job_texts:
            self.job_vectors = self.vectorizer.fit_transform(self.job_texts)
        else:
            self.job_vectors = None

    def _calculate_skill_match_score(self, resume_skills, job_skills):
        """
        Calculate skill match score between resume and job.

        Args:
            resume_skills (list): Skills from resume
            job_skills (list): Required skills for job

        Returns:
            dict: Match statistics
        """
        resume_skills_set = set(s.lower() for s in resume_skills)
        job_skills_set = set(s.lower() for s in job_skills)

        matched_skills = resume_skills_set & job_skills_set
        missing_skills = job_skills_set - resume_skills_set
        extra_skills = resume_skills_set - job_skills_set

        if len(job_skills_set) > 0:
            match_percentage = (len(matched_skills) / len(job_skills_set)) * 100
        else:
            match_percentage = 0

        return {
            'matched_skills': sorted(list(matched_skills)),
            'missing_skills': sorted(list(missing_skills)),
            'extra_skills': sorted(list(extra_skills)),
            'match_percentage': round(match_percentage, 2),
            'total_required': len(job_skills_set),
            'total_matched': len(matched_skills)
        }

    def _calculate_experience_match(self, resume_level, job_level):
        """
        Calculate experience level compatibility.

        Args:
            resume_level (str): Experience level from resume
            job_level (str): Experience level required for job

        Returns:
            float: Compatibility score (0-1)
        """
        levels = {
            'Junior': 1,
            'Mid-Level': 2,
            'Senior': 3,
            'Unknown': 2
        }

        resume_val = levels.get(resume_level, 2)
        job_val = levels.get(job_level, 2)

        # Calculate compatibility
        if resume_val >= job_val:
            return 1.0  # Overqualified or perfect match
        elif job_val - resume_val == 1:
            return 0.7  # Slightly underqualified but possible
        else:
            return 0.4  # Significantly underqualified

    def get_recommendations(self, resume_data, top_n=5, min_skill_match=30):
        """
        Get job recommendations based on resume.

        Args:
            resume_data (dict): Parsed resume data from ResumeParser
            top_n (int): Number of recommendations to return
            min_skill_match (float): Minimum skill match percentage (0-100)

        Returns:
            list: Ranked job recommendations with match scores
        """
        if not self.jobs:
            return []

        # Create text representation of resume
        resume_text = f"{resume_data['cleaned_text']} {' '.join(resume_data['skills'])}"

        # Transform resume to vector
        resume_vector = self.vectorizer.transform([resume_text])

        # Calculate cosine similarity
        similarities = cosine_similarity(resume_vector, self.job_vectors).flatten()

        recommendations = []

        for idx, job in enumerate(self.jobs):
            # Calculate skill match
            skill_match = self._calculate_skill_match_score(
                resume_data['skills'],
                job['required_skills']
            )

            # Skip jobs below minimum skill match threshold
            if skill_match['match_percentage'] < min_skill_match:
                continue

            # Calculate experience match
            exp_match = self._calculate_experience_match(
                resume_data.get('experience_level', 'Unknown'),
                job.get('experience_level', 'Unknown')
            )

            # Calculate combined score
            # Weight: 40% skill match, 40% content similarity, 20% experience match
            combined_score = (
                0.4 * (skill_match['match_percentage'] / 100) +
                0.4 * similarities[idx] +
                0.2 * exp_match
            ) * 100

            recommendations.append({
                'job': job,
                'match_score': round(combined_score, 2),
                'skill_match': skill_match,
                'content_similarity': round(similarities[idx] * 100, 2),
                'experience_match': round(exp_match * 100, 2),
                'rank': 0  # Will be set after sorting
            })

        # Sort by combined score (descending)
        recommendations.sort(key=lambda x: x['match_score'], reverse=True)

        # Add rank and limit results
        for i, rec in enumerate(recommendations[:top_n], 1):
            rec['rank'] = i

        return recommendations[:top_n]

    def get_job_by_id(self, job_id):
        """
        Get a specific job by ID.

        Args:
            job_id (int): Job ID

        Returns:
            dict: Job data or None if not found
        """
        for job in self.jobs:
            if job['id'] == job_id:
                return job
        return None

    def get_all_skills(self):
        """
        Get all unique skills from the job database.

        Returns:
            set: All unique skills
        """
        all_skills = set()
        for job in self.jobs:
            all_skills.update(job['required_skills'])
        return all_skills


if __name__ == '__main__':
    engine = JobRecommendationEngine()
    print(f"Loaded {len(engine.jobs)} jobs from database")
    print(f"Total unique skills: {len(engine.get_all_skills())}")
