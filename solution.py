import time
import json
import requests
from flask import Flask, request, jsonify
from tigrmail import Tigrmail
from google import genai
from threading import Thread

# ---------------- CONFIG ----------------
TIGRMAIL_TOKEN = "test_email_token"
TIGRMAIL_INBOX = "test_email" 
GEMINI_API_KEY = "AI_tool_token"  
MODEL_NAME = "gemini-3-flash-preview"
CRM_PORT = 5000

# ---------------- INIT ----------------
tigrmail = Tigrmail(token=TIGRMAIL_TOKEN)
client = genai.Client(api_key=GEMINI_API_KEY)

# ---------------- FLASK CRM ----------------
app = Flask(__name__)
applications = []

@app.route("/", methods=["POST"])
def add_application():
    data = request.get_json()
    applications.append(data)
    print("\nReceived JSON in CRM:")
    print(json.dumps(data, indent=2))
    return jsonify({"status": "ok"}), 200

@app.route("/show", methods=["GET"])
def show_applications():
    return jsonify(applications), 200

# Flask starting
def run_crm():
    app.run(port=CRM_PORT, debug=False, use_reloader=False)

Thread(target=run_crm).start()
print(f"CRM running on http://127.0.0.1:{CRM_PORT}")
time.sleep(1) # wait one second for server start

# ---------------- WAIT FOR EMAIL ----------------
print(f"Waiting for message: {TIGRMAIL_INBOX}")
message = None
while not message:
    try:
        message = tigrmail.poll_next_message(inbox=TIGRMAIL_INBOX)
    except Exception:
        time.sleep(5)

print("\n📨 Email received!")
print("Subject:", message['subject'])
print("Body:", message['body'])

# ---------------- PROCESS WITH GEMINI ----------------
body = message['body']
prompt = f"""
Extract structured data from the following loan application text. 
Return JSON with fields: first_name, last_name, email, loan_amount, purpose.
Text: {body}
"""

try:
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )
    output_text = response.text.strip()
    if output_text.startswith("```json"):
        output_text = output_text[len("```json"):].strip()
    if output_text.endswith("```"):
        output_text = output_text[:-3].strip()
    data_json = json.loads(output_text)
except Exception as e:
    print("Error processing AI:", e)
    data_json = None

# ---------------- SEND TO CRM ----------------
if data_json:
    try:
        r = requests.post(f"http://127.0.0.1:{CRM_PORT}", json=data_json)
        print("Data sent to CRM, status:", r.status_code)
    except Exception as e:
        print("Error sending to CRM:", e)

    # ---------------- SIMULATED CONFIRMATION ----------------
    confirmation_subject = "Your loan application was processed"
    confirmation_body = f"Your application has been processed successfully:\n\n{json.dumps(data_json, indent=2)}"
    print(f"\nProcess completed. Data from email:")
    print(json.dumps(data_json, indent=2))
    print("\nConfirmation email would be sent here (simulated).")

# ---------------- KEEP SCRIPT RUNNING ----------------
print("\nCRM is live. Go to http://127.0.0.1:5000/show to see all processed applications.")
print("Script will keep running to process next emails...\n")

while True:
    time.sleep(10)