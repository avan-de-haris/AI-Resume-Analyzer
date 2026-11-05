
import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("BASE_URL"),
    timeout=180.0,
    max_retries=2
)


def analyze_resume(resume_text, user_goal):

    prompt = f"""
You are a senior hiring manager and career coach.

Analyze the following resume for the user's desired career role.

Desired Role: {user_goal}

STRICT RULES:
1. Extract skills relevant to the desired role.
2. Identify genuinely missing skills.
3. Generate a learning roadmap only for missing skills.
4. Generate relevant interview questions.
5. Avoid irrelevant skills.
6. Be specific and actionable.

Return valid JSON using exactly this structure:

{{
    "skills": [],
    "missing_skills": [],
    "roadmap": [],
    "interview_questions": []
}}

RESUME:
{resume_text}
"""

    try:
        print("DEBUG: Sending resume to Gemini...")
        print("DEBUG: Resume length:", len(resume_text))

        response = client.chat.completions.create(
            model="gemini-2.0-flash",
            reasoning_effort="low",
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional hiring manager."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            response_format={"type": "json_object"}
        )

        content = response.choices[0].message.content

        if not content:
            raise ValueError("Gemini returned an empty response.")

        result = json.loads(content)

        print("DEBUG: Resume analysis completed successfully.")

        return result

    except Exception as e:

        print("AI API ERROR:", repr(e))
        print("STATUS CODE:", getattr(e, "status_code", None))
        print("ERROR BODY:", getattr(e, "body", None))

        return {
            "skills": [],
            "missing_skills": [],
            "roadmap": [],
            "interview_questions": [],
            "error": str(e)
        }
