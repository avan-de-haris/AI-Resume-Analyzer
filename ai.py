from openai import OpenAI

client = OpenAI()

def analyze_resume(resume_text, user_goal):
    prompt = f"""
    you are a senior software engineer and a career coach. I will provide you with a resume and a user goal. Please analyze the resume and provide feedback on how well it aligns with the user's goal. Offer suggestions for improvement, highlight strengths, and identify any gaps or areas that need attention. Be specific and actionable in your feedback.
    evaluate the resume based on users goal
    user goal: "{user_goal}"

    STRICT RULES:
    - Extract only the relevant information that pertains to the user's goal.
    - Remove irrelevant tools [excel for backend, etc]
    - Identify real gaps
    - Generate Roadmap only for missing feilds
    - Make output Different based on the user goal

    Return only json:
    {{
    "skills": [],
    "missing_skills": [],
    "roadmap": [],
    "interview_questions": [],

    }}
    Resume:
    {resume_text}

    """
        

