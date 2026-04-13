#!/usr/bin/env python3
"""
Job Recommendation System - Main Entry Point

This script provides a command-line interface for the job recommendation system.
It takes a PDF resume as input and recommends matching job positions.

Usage:
    python main.py --resume path/to/resume.pdf
    python main.py --resume path/to/resume.pdf --top 10 --min-match 20
"""

import argparse
import sys
from resume_parser import ResumeParser
from recommendation_engine import JobRecommendationEngine


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")


def print_section(text):
    """Print a section header."""
    print(f"\n{'─' * 50}")
    print(f"  {text}")
    print(f"{'─' * 50}")


def print_job_recommendation(rec, detailed=False):
    """
    Print a job recommendation in a formatted way.

    Args:
        rec (dict): Recommendation data
        detailed (bool): Whether to show detailed information
    """
    job = rec['job']
    skill_match = rec['skill_match']

    print(f"\n{'#' * 60}")
    print(f"  #{rec['rank']} | {job['title']}")
    print(f"{'#' * 60}")
    print(f"  Company:    {job['company']}")
    print(f"  Location:   {job['location']}")
    print(f"  Salary:     {job['salary']}")
    print(f"  Level:      {job['experience_level']}")
    print(f"\n  ── Match Score: {rec['match_score']}% ──")
    print(f"     • Content Similarity: {rec['content_similarity']}%")
    print(f"     • Skill Match:        {skill_match['match_percentage']}% ({skill_match['total_matched']}/{skill_match['total_required']})")
    print(f"     • Experience Match:   {rec['experience_match']}%")

    if detailed:
        print(f"\n  Description:")
        print(f"  {job['description']}")

        print(f"\n  ✅ Matched Skills ({len(skill_match['matched_skills'])}):")
        if skill_match['matched_skills']:
            skills_text = ', '.join(skill_match['matched_skills'])
            print(f"  {skills_text}")
        else:
            print("  None")

        print(f"\n  📋 Missing Skills ({len(skill_match['missing_skills'])}):")
        if skill_match['missing_skills']:
            skills_text = ', '.join(skill_match['missing_skills'])
            print(f"  {skills_text}")
        else:
            print("  None - You have all required skills!")

        if skill_match['extra_skills']:
            print(f"\n  ⭐ Extra Skills You Have ({len(skill_match['extra_skills'])}):")
            skills_text = ', '.join(skill_match['extra_skills'][:10])  # Limit to 10
            print(f"  {skills_text}")


def main():
    """Main function to run the job recommendation system."""
    parser = argparse.ArgumentParser(
        description='Job Recommendation System - Find jobs matching your resume',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --resume my_resume.pdf
  python main.py --resume my_resume.pdf --top 10
  python main.py --resume my_resume.pdf --min-match 50 --detailed
        """
    )

    parser.add_argument(
        '--resume', '-r',
        required=True,
        help='Path to your resume PDF file'
    )

    parser.add_argument(
        '--top', '-t',
        type=int,
        default=5,
        help='Number of job recommendations to show (default: 5)'
    )

    parser.add_argument(
        '--min-match', '-m',
        type=float,
        default=20,
        help='Minimum skill match percentage (0-100, default: 20)'
    )

    parser.add_argument(
        '--detailed', '-d',
        action='store_true',
        help='Show detailed information including skill breakdowns'
    )

    parser.add_argument(
        '--database', '-db',
        default='job_database.json',
        help='Path to job database JSON file (default: job_database.json)'
    )

    args = parser.parse_args()

    try:
        # Print welcome header
        print_header("🎯 Job Recommendation System")
        print("Analyzing your resume and finding the best job matches...")

        # Step 1: Parse the resume
        print_section("Step 1: Parsing Resume")
        resume_parser = ResumeParser()
        print(f"Loading PDF: {args.resume}")
        resume_data = resume_parser.parse_resume(args.resume)

        print(f"✓ Successfully parsed resume: {resume_data['file_name']}")
        print(f"  • Detected Experience Level: {resume_data['experience_level']}")
        print(f"  • Skills Found: {resume_data['skill_count']}")

        if args.detailed:
            print(f"\n  Extracted Skills:")
            skills_text = ', '.join(resume_data['skills'])
            print(f"  {skills_text}")

        # Step 2: Load recommendation engine
        print_section("Step 2: Loading Job Database")
        engine = JobRecommendationEngine(args.database)
        print(f"✓ Loaded {len(engine.jobs)} jobs from database")

        # Step 3: Get recommendations
        print_section("Step 3: Generating Recommendations")
        print(f"Finding top {args.top} matches with minimum {args.min_match}% skill match...\n")

        recommendations = engine.get_recommendations(
            resume_data,
            top_n=args.top,
            min_skill_match=args.min_match
        )

        # Step 4: Display results
        if not recommendations:
            print("❌ No job recommendations found matching your criteria.")
            print(f"   Try lowering --min-match (current: {args.min_match}%)")
            print(f"   Or your resume may need more relevant skills.")
            return 1

        print(f"✓ Found {len(recommendations)} matching job(s)!\n")

        for rec in recommendations:
            print_job_recommendation(rec, detailed=args.detailed)

        # Print summary
        print_header("📊 Summary")
        print(f"Resume: {resume_data['file_name']}")
        print(f"Your Experience Level: {resume_data['experience_level']}")
        print(f"Skills Detected: {resume_data['skill_count']}")
        print(f"Jobs Recommended: {len(recommendations)}")

        avg_match = sum(r['match_score'] for r in recommendations) / len(recommendations)
        print(f"Average Match Score: {avg_match:.1f}%")

        print("\n" + "=" * 70)
        print("Recommendation complete! Good luck with your job search! 🚀")
        print("=" * 70 + "\n")

        return 0

    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


def interactive_mode():
    """Run the recommendation system in interactive mode."""
    print_header("🎯 Job Recommendation System - Interactive Mode")
    print("\nThis tool will analyze your resume and recommend matching jobs.\n")

    resume_path = input("Enter the path to your resume PDF: ").strip()

    try:
        top_n = int(input("How many recommendations? (default: 5): ") or "5")
    except ValueError:
        top_n = 5

    try:
        min_match = float(input("Minimum skill match %? (default: 20): ") or "20")
    except ValueError:
        min_match = 20

    detailed = input("Show detailed info? (y/N): ").strip().lower() == 'y'

    # Create mock args
    class Args:
        pass

    args = Args()
    args.resume = resume_path
    args.top = top_n
    args.min_match = min_match
    args.detailed = detailed
    args.database = 'job_database.json'

    # Override sys.argv and call main
    sys.argv = ['main.py']

    # Run the main logic manually
    resume_parser = ResumeParser()
    print(f"\nParsing resume: {resume_path}")
    resume_data = resume_parser.parse_resume(resume_path)

    print(f"✓ Found {resume_data['skill_count']} skills")
    print(f"  Experience Level: {resume_data['experience_level']}")

    engine = JobRecommendationEngine(args.database)
    recommendations = engine.get_recommendations(
        resume_data,
        top_n=args.top,
        min_skill_match=args.min_match
    )

    for rec in recommendations:
        print_job_recommendation(rec, detailed=args.detailed)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        sys.exit(main())
    else:
        interactive_mode()
