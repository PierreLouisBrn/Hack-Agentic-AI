# 🛡️ DeepFender – Your Data Defender

![DeepFender Logo](assets/deepfender-logo.png)

DeepFender is a next-generation agentic AI system that autonomously monitors, analyzes, and protects your emails against phishing, fraud, and malicious content — from inbox to intelligence, with zero user friction.
 DeepFender acts as an intelligent surcouche sécurisée for your email inbox (Gmail, etc.).
 
- It automatically:
- Retrieves and pre-processes new emails
- Flags potential phishing/fraud attempts
- Analyzes language, links, attachments (PDF, executables…)
- Executes suspicious links in a virtual sandbox
- Stores summaries and decisions securely (AWS)
- Can be controlled by voice or prompt


✅ Multi-agent pipeline with modular autonomy
📬 Real-time Gmail monitoring via OAuth 2.0
🧠 Email classification (tone, structure, urgency, link behavior)
📄 Summarization and threat rationale generation
📎 Attachment analysis (PDF scanner)
🔗 Safe sandbox testing for links
🗣️ Voice-activated control (Whisper + Open Interpreter)
📦 Long-term vector memory (FAISS)
☁️ Secure cloud storage (AWS DynamoDB)

DeepFender is a next-generation, autonomous AI-powered email security solution designed to detect, analyze, and mitigate phishing and malicious content in real time. With a modular, multi-agent architecture and seamless integration with cloud services, DeepFender protects your inbox from evolving threats — from email ingestion to detailed risk reporting.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Overview

DeepFender acts as an intelligent security overlay for your email inbox. It automatically retrieves and pre-processes emails, analyzes content, links, and attachments via specialized agents, and generates detailed reports on potential phishing threats. With multi-modal capabilities and voice command integration, DeepFender delivers a proactive and adaptive defense for your communications.

---

## Features

- **Real-Time Email Monitoring:**  
  Uses Gmail API with OAuth 2.0 to fetch emails automatically.
  
- **Multi-Agent Analysis:**  
  - *Email Scanner:* Extracts email content and metadata.  
  - *NLP Analyzer:* Performs natural language analysis to detect urgent language, manipulation, and phishing signals.  
  - *Link Checker:* Extracts and evaluates hyperlinks, optionally testing them in a secure sandbox.  
  - *Report Generator:* Synthesizes analysis results into a comprehensive risk report.
  
- **Voice Command Interface:**  
  Control DeepFender with voice commands using speech-to-text (Whisper) and text-to-speech (pyttsx3).

- **Long-Term Memory & Adaptive Learning:**  
  Uses vector memory (FAISS/Chroma) to store historical analysis data for improved threat detection over time.

- **Cloud Integration:**  
  Stores analysis results in AWS DynamoDB/S3 and leverages AWS Bedrock (e.g., with Mistral) for LLM-based analysis.

- **User-Friendly Dashboard:**  
  (Optional) Visualize alerts, threat levels, and trends via a Streamlit/Gradio dashboard.

---

## Architecture



---

## Tech Stack

- **Backend:** Python, LangGraph, LangChain
- **Multi-Agent Orchestration:** Custom Python agents integrated via LangGraph
- **Email Integration:** Gmail API (OAuth 2.0)
- **LLM:** Mistral 7B via AWS Bedrock or similar
- **Voice Interface:** Whisper for speech-to-text, pyttsx3 for TTS
- **Vector Memory:** FAISS or Chroma for contextual learning
- **Cloud Services:** AWS DynamoDB, S3, Bedrock
- **PDF & Attachment Analysis:** pdfid.py, PyMuPDF
- **Dashboard:** Streamlit or Gradio (optional)

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/deepfender.git
cd deepfender

 Create and Activate a Virtual Environment

python -m venv .venv```

# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

3. Install Dependencies

pip install -r requirements.txt

    Note: If you encounter issues installing pyaudio, consider using pipwin on Windows.

4. Configure Environment Variables

Create a .env file at the project root with your configuration:

# Gmail API credentials
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GOOGLE_REFRESH_TOKEN=your_google_refresh_token

# AWS Credentials
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_REGION_NAME=eu-west-3
DYNAMODB_TABLE_NAME=deepfender-emails

# LLM & Model configuration
MODEL=mistral/mixtral-8x7b-instruct-v0:1

# Sandbox API (for link testing)
SANDBOX_API_KEY=your_sandbox_api_key

    Important: Add .env to your .gitignore to protect your credentials.

Usage
Launching Email Monitoring

Start the Gmail trigger to monitor your inbox:

python trigger_gmail.py

This script authenticates with Gmail, retrieves new emails, extracts headers, links, attachments, and passes data to the multi-agent workflow.
Running the Main Workflow

Execute the main graph that orchestrates agent processing:

python main.py

This flow processes an email through the following steps:

    Email Scanning: Extract content and metadata.

    NLP Analysis: Analyze tone, urgency, and phishing signals.

    Link Analysis: Extract and assess hyperlinks.

    Report Generation: Compile results into a final risk report.

(Optional) Running the Dashboard

If a dashboard is implemented, launch it with:

streamlit run ui/dashboard.py


Key Functions and Modules
File	Key Function	Description
trigger_gmail.py	get_latest_inbox_email()	Retrieves email headers, links, attachments
agents/email_scanner.py	scan_email()	Extracts email content and metadata
agents/nlp_analyzer.py	analyze_text()	Performs NLP analysis on email content
agents/link_analyzer.py	analyze_links()	Extracts and assesses hyperlink safety
agents/report_generator.py	generate_report()	Compiles a final risk report
tools/gmail_watcher.py	-	Connects to Gmail API to retrieve emails
utils/dynamo.py	save_to_dynamodb()	Saves analysis results to AWS DynamoDB
memory/	-	Stores historical analysis (vector DB)
ui/dashboard.py	-	(Optional) Dashboard for live monitoring



Optional Advanced Features

    Voice Command Interface:
    Use Whisper (speech-to-text) and pyttsx3 (TTS) to control DeepFender via voice commands.

    Long-Term Memory & Adaptive Learning:
    Store historical analysis in a vector DB (FAISS/Chroma) to refine threat detection.

    Sandbox Testing:
    Dynamically test suspicious links or attachments in an isolated environment.

    Automated Incident Response:
    Integrate with AWS Lambda/EventBridge for real-time threat mitigation.

Roadmap

    Phase 1: Complete MVP with email ingestion, multi-agent analysis, and reporting.

    Phase 2: Integrate voice commands and sandbox testing.

    Phase 3: Develop a real-time dashboard and advanced memory for adaptive learning.

    Phase 4: Expand integrations with other email platforms and build an API for enterprise use.


