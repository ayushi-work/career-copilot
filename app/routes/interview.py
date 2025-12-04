import json
import re
import boto3
from fastapi import APIRouter, HTTPException, Form
import os
from dotenv import load_dotenv

load_dotenv()

AWS_REGION = os.getenv("AWS_REGION")
MODEL_ID = os.getenv("BEDROCK_MODEL")

bedrock = boto3.client("bedrock-runtime", region_name=AWS_REGION)

# ⭐ THIS MUST EXIST — FastAPI needs this
router = APIRouter()


@router.post("/interview/generate")
async def generate_interview(
    role: str = Form(...),
    company: str = Form(...),
    level: str = Form(...),
    audio: bool = Form(...)
):
    """
    Generates interview questions using Titan Text Lite and returns structured JSON.
    """

    prompt = f"""
    Generate structured interview questions for a {level}-level {role} applying at {company}.
    Return STRICT JSON with the following structure only:

    {{
      "questions": [
        {{
          "question": "string",
          "answer": "string",
          "followups": ["string"],
          "difficulty": "easy|medium|hard"
        }}
      ]
    }}

    DO NOT return explanations. DO NOT return text outside JSON.
    """

    try:
        response = bedrock.invoke_model(
            modelId=MODEL_ID,
            body=json.dumps({
                "inputText": prompt,
                "textGenerationConfig": {
                    "maxTokenCount": 1200,
                    "temperature": 0.2,
                    "topP": 0.9
                }
            })
        )
    except Exception as e:
        raise HTTPException(500, f"Bedrock Error: {str(e)}")

    raw_output = response["body"].read().decode()

    print("\n========== RAW MODEL OUTPUT ==========")
    print(raw_output)
    print("======================================\n")

    # Extract JSON only
    match = re.search(r"\{.*\}", raw_output, flags=re.DOTALL)

    if not match:
        raise HTTPException(
            500,
            "Model returned unexpected structure. Cannot find JSON."
        )

    cleaned = match.group(0)

    print("\n===== CLEANED JSON =====")
    print(cleaned)
    print("========================\n")

    try:
        result_json = json.loads(cleaned)
    except Exception as e:
        raise HTTPException(
            500,
            f"JSON decode error: {str(e)}"
        )

    return {
        "success": True,
        "analysis": result_json,
        "raw_output": raw_output
    }
