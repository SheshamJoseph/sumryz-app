# Sumryz

Sumryz is an AI-powered web application that helps students quickly summarize lecture notes and documents into concise, easy-to-read bullet points. Upload your files or paste text, and let Sumryz turn hours of content into minutes of clarity.

## Features

- **AI Summarization:** Uses Cohere's AI to generate structured summaries from lecture notes.
- **File Upload:** Supports PDF, DOCX, and TXT files.
- **Secure Authentication:** Register, login, reset password, and delete account.
- **Document Management:** Download or delete your generated summaries.
- **Modern UI:** Clean, responsive interface for desktop and mobile.

## Getting Started

### Prerequisites

- Python 3.10+
- [Cohere API Key](https://cohere.com/)
- SMTP credentials for email (Gmail recommended)

### Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/sumryz.git
   cd sumryz
   ```

2. **Create a virtual environment and activate it:**
   ```sh
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   - Copy `.env_example` to `.env` and fill in your secrets:
     ```
     SECRET_KEY=your_secret_key
     COHERE_API_KEY=your_cohere_api_key
     ```

### Running the App

1. **Initialize the database:**
   ```sh
   flask init-db
   ```

2. **Start the development server:**
   ```sh
   flask run
   ```
   Or:
   ```sh
   python app.py
   ```

3. **Access Sumryz:**
   Open [http://localhost:5000](http://localhost:5000) in your browser.


## Folder Structure

```
app.py
app/
    __init__.py
    models.py
    auth/
    main/
    templates/
    static/
config.py
requirements.txt
.env
tests/
```

## Credits

- [Cohere](https://cohere.com/) for AI summarization
- Flask, SQLAlchemy, Flask-Login, Flask-Mail, Flask-WTF

---
Sumryz: Turn hours of lectures into minutes of clarity.
