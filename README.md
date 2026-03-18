# finance-fund-AI-automation
## 📩 Loan Application Automation System

### 📌 Overview

This project automates the processing of loan applications received via email. It was designed to replace manual workflows in a financial services company (FinServe), where employees had to re-enter data, prepare documents, and track applications manually.

The solution uses Python and Gemini AI to extract structured data from emails and store it in a simple CRM.

### 🚀 Key Features

- 📥 Email polling and content extraction

- 🤖 AI-based data structuring (Gemini API)

- 🗂️ Lightweight CRM built with Flask

- 🔗 Easy integration via HTTP (REST API)

- 🔄 Continuous real-time processing

### ⚙️ How It Works

- The script monitors an email inbox (Tigrmail)

- A new email is received → content is extracted

- Gemini AI converts text into structured JSON:

    - First name
  
    - Last name
  
    - Email
  
    - Loan amount
  
    - Purpose

- Data is sent to a local Flask CRM

- Applications are stored and accessible via API

### 🛠️ Tech Stack

- Python

- Flask
  
- Gemini API

- Tigrmail API
  
- requests, imaplib, email

### 💡 Business Value

- ⏱️ Saves time (no manual data entry)

- 📈 Improves productivity

- 🔄 Standardizes data processing

- 🤖 Introduces AI into operations
