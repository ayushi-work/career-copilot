Here is a **fully polished, GitHub-optimized README with badges + perfect copy-paste formatting + code fences everywhere.**
You can paste this **directly** into your `README.md`.

---

# 🚀 GenAI Career Copilot

### *AI-powered Resume, Job Match & Interview Assistant built with FastAPI + AWS Bedrock*


---

# 📌 Overview

**GenAI Career Copilot** is an AI-powered FastAPI application integrated with AWS Bedrock, Rekognition, S3, and Textract to automate:

✔ Resume generation
✔ Job description analysis
✔ Mock interview generation
✔ Face recognition login
✔ Secure S3 document storage
✔ Optional document text extraction

---

# 🌟 Features

### ✅ **Face Login (Rekognition)**

* Upload face → stored in S3
* Compared with Rekognition Face Collection
* Auth success when similarity ≥ **90%**

---

### ✅ **Resume Generator (Bedrock Titan + FPDF + S3)**

* Creates **ATS-friendly resumes**
* Supports multiple variations
* Automatically exported to **PDF**
* Uploads to S3 and returns pre-signed URL

---

### ✅ **Job Description Analyzer**

Extracts and returns JSON:

```json
{
  "key_responsibilities": [],
  "required_skills": [],
  "missing_skills": [],
  "match_percentage": 0,
  "recommendations": []
}
```

---

### ✅ **Mock Interview Generator**

Generates 6–10 questions with:

* Difficulty level
* Ideal sample answers

---

### ✅ **Textract Document Parsing (Optional)**

* Extracts text
* Auto-fills resume fields

---

# 🏗️ System Architecture

```
User
│
│  HTML / CSS / JS Frontend
▼
FastAPI Backend ───────────────────────────┐
│                                          │
├── Resume Generator → Bedrock (Titan)     │
├── Job Analyzer     → Bedrock (Titan)     │
├── Interview Gen    → Bedrock (Titan)     │
├── Face Login       → Rekognition         │
├── PDF Maker        → FPDF                │
└── Storage          → S3                  │
                                           ▼
                                    AWS Cloud
```

---

# 🔧 Tech Stack

### **Backend**

* Python
* FastAPI
* boto3
* FPDF
* Amazon Bedrock SDK

### **Frontend**

* HTML
* CSS
* JavaScript (Fetch API)

### **AWS Services**

* Amazon Bedrock (Titan LLM)
* S3
* Rekognition
* Textract
* IAM

---

# 📁 Project Structure

```
genai-career-copilot/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── routes/
│   │   │   ├── interview.py
│   │   │   └── textract.py   # optional
│   ├── .env
│   ├── venv/
│   └── requirements.txt
│
└── frontend/
    ├── index.html
    ├── style.css
    └── app.js
```

---

# 🔐 Environment Variables (`backend/.env`)

```
AWS_REGION=us-east-1
S3_BUCKET=career-copilot-bucket
REKOG_COLLECTION_ID=copilot-users
BEDROCK_MODEL=amazon.titan-text-lite-v1
```

---

# ▶️ Running the Backend

### **1️⃣ Activate Virtual Env**

```bash
cd backend
source venv/bin/activate
```

### **2️⃣ Install Dependencies**

```bash
pip install -r requirements.txt
```

### **3️⃣ Run FastAPI**

```bash
uvicorn app.main:app --reload --port 8000
```

---

# 🌐 Running the Frontend

Just open:

```
frontend/index.html
```

Or run via **VS Code Live Server**.

---

# 📌 Core API Endpoints

---

## 🔹 **Face Login**

**POST** `/auth/login-face`

```bash
curl -X POST "http://127.0.0.1:8000/auth/login-face" \
  -F "image=@selfie.jpg"
```

---

## 🔹 **Generate Resume**

**POST** `/resume/generate`

Example:

```bash
curl -X POST http://127.0.0.1:8000/resume/generate \
-F "name=Ayushi" \
-F "email=ayushi@example.com" \
-F "skills=Python, AWS, FastAPI" \
-F "experience=2 years backend experience"
```

---

## 🔹 **Analyze Job Description**

**POST** `/job/analyze`

Example:

```bash
curl -X POST http://127.0.0.1:8000/job/analyze \
-F "job_description=We need a Python engineer..." \
-F "skills=Python, AWS" \
-F "experience=2 years"
```

---

## 🔹 **Mock Interview Generator**

**POST** `/interview/generate`

Sample response:

```json
{
  "questions": [
    {
      "question": "Explain Python decorators.",
      "difficulty": "medium",
      "ideal_answer": "A decorator modifies the behavior of a function..."
    }
  ]
}
```

---

# 📤 S3 Storage Structure

All resumes saved as:

```
s3://career-copilot-bucket/resumes/<uuid>.pdf
```

Configure:

* Public access
* Pre-signed URLs
* Lifecycle policies

---

# 🚀 Deployment Options

### **Backend**

* AWS Elastic Beanstalk
* AWS ECS Fargate
* AWS Lambda + API Gateway
* EC2 (manual deploy)

### **Frontend**

* S3 Static Website Hosting
* CloudFront CDN

---

# 🔮 Future Enhancements

* Full dashboard UI
* Voice-based interviews (Transcribe)
* Resume scoring engine
* HR candidate ranking
* LLM chat-style assistant
* OAuth login (Google, LinkedIn)

---

# 🏁 Conclusion

**GenAI Career Copilot** is a complete AI-powered solution for:

✔ Resume creation
✔ Job description matching
✔ Interview preparation
✔ Secure face login
✔ Document extraction

Designed using scalable **AWS cloud services** and a clean **FastAPI backend**.

---

If you'd like:

✅ **Full PPT (20–25 slides)**
✅ **High-quality architecture diagram**
✅ **API documentation (Swagger-style)**
✅ **Project logo / branding**

Just tell me **"generate PPT"** or **"generate diagram"** 🔥
