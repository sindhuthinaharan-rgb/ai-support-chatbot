# AI-Powered Customer Support Chatbot

An intelligent hybrid AI Customer Support Chatbot built with Python, Flask, SQLite, and Google Gemini API.

## Features
- **Two-Tier Architecture**: Instant response for local FAQs to save API quota and AI-powered responses for complex user queries.
- **Context Awareness**: Maintains conversation history using SQLite database integration.
- **Error Handling**: Includes a fallback mechanism in case of API rate limits or network errors.
- **Web Interface**: Simple, interactive, and user-friendly HTML/CSS chat UI.

## Tech Stack
- **Backend**: Python, Flask
- **AI Model**: Google Gemini API (`gemini-3.6-flash`)
- **Database**: SQLite
- **Frontend**: HTML5, CSS3, JavaScript

## How to Run Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/sindhuthinaharan-rgb/ai-support-chatbot.git
   cd ai-support-chatbot
   pip install flask google-genai
   python app.py
