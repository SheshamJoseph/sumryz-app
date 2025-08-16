import os
import docx
from pypdf import PdfReader

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}

def extract_text_from_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == '.txt':
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
        
    elif ext == '.pdf':
        reader = PdfReader(file_path)
        text = ''
        for page in reader.pages:
            text += page.extract_text() + '\n'
        return text
    
    elif ext == '.docx':
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    
    else:
        raise ValueError("Unsupported file type: {}".format(ext))
    
    
    
def allowed_files(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def cohere_summarizer(text_document):
    import cohere
    from cohere import UserChatMessageV2
    from dotenv import load_dotenv
    
    # load environment variables from .env file
    load_dotenv()
    
    COHERE_API_KEY = os.getenv('COHERE_API_KEY')
    if not COHERE_API_KEY:
        raise ValueError("Cohere API key not found in environment variables.")
    
    
    client = cohere.ClientV2(api_key=COHERE_API_KEY)
    message = f"Summarize the following text into concise, well-strucutured notes. Use bullet points where helpful. Highlight the main ideas, key terms, and important concepts, avoiding unnecessary specifics. Keep the summary clear and easy to scan.\n\n{text_document}"
    
    response = client.chat(
        model="command-a-03-2025",
        messages=[UserChatMessageV2(role="user", content=message)],
    )

    return response.message.content if response.message else "No summary generated."
