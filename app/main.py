from fastapi import FastAPI, UploadFile, File, Form
import boto3
import uuid
import os
import json
import re
from dotenv import load_dotenv
from fpdf import FPDF

# Load env
load_dotenv()

AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET = os.getenv("S3_BUCKET")
REKOG_COLLECTION = os.getenv("REKOG_COLLECTION_ID")
MODEL_ID = os.getenv("BEDROCK_MODEL")

# AWS clients
s3 = boto3.client("s3", region_name=AWS_REGION)
rekog = boto3.client("rekognition", region_name=AWS_REGION)
bedrock = boto3.client("bedrock-runtime", region_name=AWS_REGION)

# MAIN FASTAPI APP — DEFINE ONLY ONCE
app = FastAPI()


@app.get("/")
def home():
    return {"message": "Career Copilot Backend Running"}


# -----------------------------------------------------------
# FACE LOGIN
# -----------------------------------------------------------
@app.post("/auth/login-face")
async def login_face(image: UploadFile = File(...)):
    temp_filename = f"/tmp/{uuid.uuid4()}.jpg"

    with open(temp_filename, "wb") as f:
        f.write(await image.read())

    s3_key = f"auth-temp/{uuid.uuid4()}.jpg"
    s3.upload_file(temp_filename, S3_BUCKET, s3_key)

    response = rekog.search_faces_by_image(
        CollectionId=REKOG_COLLECTION,
        Image={"S3Object": {"Bucket": S3_BUCKET, "Name": s3_key}},
        FaceMatchThreshold=90,
        MaxFaces=1
    )

    os.remove(temp_filename)

    matches = response.get("FaceMatches", [])
    if len(matches) == 0:
        return {"success": False, "message": "Face not recognized"}

    matched_id = matches[0]["Face"]["ExternalImageId"]

    return {
        "success": True,
        "user": matched_id,
        "similarity": matches[0]["Similarity"]
    }


# -----------------------------------------------------------
# RESUME GENERATOR
# -----------------------------------------------------------
@app.post("/resume/generate")
async def generate_resume(
    name: str = Form(...),
    email: str = Form(...),
    skills: str = Form(...),
    experience: str = Form(...)
):
    prompt = f"""
    Generate an ATS-friendly resume.

    Name: {name}
    Email: {email}
    Skills: {skills}
    Experience: {experience}

    Format:
    - Summary
    - Skills
    - Experience
    - Education
    """

    response = bedrock.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps({
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": 800,
                "temperature": 0.7,
                "topP": 0.9
            }
        })
    )

    model_body = json.loads(response["body"].read())
    resume_text = model_body["results"][0]["outputText"]

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for line in resume_text.split("\n"):
        pdf.multi_cell(0, 10, line)

    filename = f"resume_{uuid.uuid4().hex}.pdf"
    pdf.output(filename)

    s3_key = f"resumes/{filename}"
    s3.upload_file(filename, S3_BUCKET, s3_key)
    os.remove(filename)

    return {"success": True, "resume_url": f"https://{S3_BUCKET}.s3.amazonaws.com/{s3_key}"}


# -----------------------------------------------------------
# JOB ANALYZER
# -----------------------------------------------------------
@app.post("/job/analyze")
async def analyze_job(
    job_description: str = Form(...),
    skills: str = Form(...),
    experience: str = Form(...)
):

    prompt = f"""
You are an expert career analyst.

Analyze the job description & return ONLY JSON:

{{
  "key_responsibilities": [],
  "required_skills": [],
  "missing_skills": [],
  "match_percentage": 0,
  "recommendations": []
}}

Job Description:
{job_description}

Skills:
{skills}

Experience:
{experience}
"""

    response = bedrock.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps({
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": 500,
                "temperature": 0.4,
                "topP": 0.9
            }
        })
    )

    body = json.loads(response["body"].read())
    raw_output = body["results"][0]["outputText"].strip()

    match = re.search(r"\{.*\}", raw_output, re.DOTALL)

    if not match:
        return {"success": False, "error": "Invalid JSON", "raw_output": raw_output}

    json_str = match.group(0)

    try:
        result_json = json.loads(json_str)
    except:
        return {"success": False, "error": "JSON parse error", "raw_json": json_str}

    return {"success": True, "analysis": result_json}


# -----------------------------------------------------------
# INTERVIEW ROUTER
# -----------------------------------------------------------
from app.routes.interview import router as interview_router
app.include_router(interview_router)
