import os
import json
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()  # Load environment variables from .env file

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("BASE_URL"),
    timeout=30.0,
    max_retries=0

)

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
    "interview_questions": []

    }}
    Resume:
    {resume_text}

    """
    try:
        response = client.chat.completions.create(
            model="gemini-3.5-flash",
            messages=[
                {"role": "system", "content": "You are a strict hiring manager."},
                {"role": "user", "content": prompt}
            ],
            response_format={
                "type": "json_object"
            }
        )
        content = response.choices[0].message.content.strip()
        start = content.find('{')
        end = content.rfind('}') + 1
        if start != -1 and end != 0:
            return json.loads(content[start:end])

        return json.loads(content)  # Return the parsed JSON response

    except Exception as e:
        return{
            "skills": [],
            "missing_skills": [],
            "roadmap": [],
            "interview_questions": [],
            "error": f"Error analyzing resume: {str(e)}"
        }

