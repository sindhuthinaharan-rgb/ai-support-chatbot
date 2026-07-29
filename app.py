import os
from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai import types
import database

app = Flask(__name__)

# Initialize SQLite DB
database.init_db()

# Replace YOUR_GEMINI_API_KEY with your actual Gemini API key from AI Studio
API_KEY = os.environ.get("GEMINI_API_KEY", "AQ.Ab8RN6Ik7apiorVrL3nB-EOQeGEB_kyE6z2MTWEybRGqkAt7Vw")
client = genai.Client(api_key=API_KEY)

# FAQ Knowledge Base
FAQS = {
    "what are your business hours?": "Our support team is available 24/7 online!",
    "how can i track my order?": "You can track your order by logging into your account and visiting the 'My Orders' section.",
    "what is your refund policy?": "We offer a 30-day full refund policy for all unused products.",
    "how do i contact human support?": "You can reach human support via email at support@example.com."
}

SYSTEM_INSTRUCTION = """
You are an intelligent, friendly Customer Support AI Assistant. 
Your goal is to help users with product inquiries, FAQs, and general support.
Keep your responses concise, clear, and polite. 
If you don't know an answer, direct them to contact support@example.com.
"""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "").strip()
    if not user_message:
        return jsonify({"response": "Please enter a message."})

    # 1. Check local FAQ first
    # 1. Check local FAQ first
    user_msg_clean = user_message.lower()
    for faq_question, faq_answer in FAQS.items():
        # Check if key words match
        if faq_question in user_msg_clean or any(word in user_msg_clean for word in ["hours", "refund", "track", "contact", "support"]):
            if any(w in user_msg_clean for w in faq_question.split()):
                database.save_chat(user_message, faq_answer)
                return jsonify({"response": faq_answer, "source": "FAQ"})

    # 2. Fetch context from history
    recent_history = database.get_recent_history(limit=3)
    conversation_prompt = ""
    for u_msg, b_msg in recent_history:
        conversation_prompt += f"User: {u_msg}\nBot: {b_msg}\n"
    conversation_prompt += f"User: {user_message}\nBot:"

    # 3. Call Gemini API with Fallback
    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=conversation_prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.7,
            ),
        )
        bot_response = response.text
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        bot_response = "I'm having trouble connecting right now. Please try again or email support@example.com."

    # 4. Save to DB
    database.save_chat(user_message, bot_response)

    return jsonify({"response": bot_response, "source": "AI"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)